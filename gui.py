import tkinter as tk
from tkinter import ttk
from config import DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT, COLORS
from material_database import MATERIALS
from drawing import DrawingManager
from calculations import calculate_radii, calculate_bend_angles, calculate_chord_length, calculate_point_coordinates
import math

class BendingCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lemez Hajlítás Kalkulátor")
        self.setup_window()
        self.create_variables()
        self.create_gui_elements()
        # Alapértelmezett anyag információk megjelenítése
        self.on_material_selected()
        # Alapértelmezett sugártípus beállítása
        self.toggle_radius_input()

    def setup_window(self):
        """Ablak beállítások"""
        self.root.state('zoomed')
        self.root.minsize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)

    def create_variables(self):
        """Változók létrehozása"""
        self.radius_type = tk.StringVar(value="inner")  # Alapértelmezett: belső sugár
        self.inner_radius = tk.StringVar()
        self.neutral_radius = tk.StringVar()
        self.outer_radius = tk.StringVar()
        self.thickness = tk.StringVar()
        self.k_factor = tk.StringVar(value="0.35")  # Alapértelmezett: 0.35
        self.segment_count = tk.StringVar()
        self.angle = tk.StringVar()
        self.start_length = tk.StringVar()
        self.end_length = tk.StringVar()
        self.material_var = tk.StringVar(value="DC04 (1.0338)")  # Alapértelmezett: DC04

    def create_gui_elements(self):
        """GUI elemek létrehozása"""
        # Scrollozható fő frame létrehozása
        canvas = tk.Canvas(self.root)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Fő frame létrehozása a canvas-en belül
        main_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=main_frame, anchor="nw")
        
        # Bal oldali panel létrehozása
        left_panel = ttk.Frame(main_frame)
        left_panel.grid(row=0, column=0, sticky="ns", padx=(10, 10))
        
        # Input mezők létrehozása
        self.create_input_fields(left_panel)
        
        # Gombok létrehozása
        self.create_buttons(left_panel)
        
        # Eredmény megjelenítő létrehozása
        self.create_result_display(left_panel)
        
        # Jobb oldali panel létrehozása
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 10))
        
        # Canvas létrehozása
        self.create_canvas(right_panel)

    def create_input_fields(self, parent):
        """Input mezők létrehozása"""
        input_frame = ttk.LabelFrame(parent, text="Adatok", padding=5)
        input_frame.pack(fill=tk.X, pady=5)
        
        # Input mezők létrehozása
        self.entries = {}
        
        # Anyagválasztó
        material_frame = ttk.LabelFrame(input_frame, text="Anyag", padding=5)
        material_frame.pack(fill=tk.X, pady=2)

        # Combobox az anyagválasztáshoz
        material_frame_inner = ttk.Frame(material_frame)
        material_frame_inner.pack(fill=tk.X, pady=2)
        ttk.Label(material_frame_inner, text="Anyag:", width=20).pack(side=tk.LEFT, padx=5)
        material_options = [f"{code} - {MATERIALS[code]['name']}" for code in MATERIALS.keys()]
        material_combo = ttk.Combobox(material_frame_inner, textvariable=self.material_var, values=material_options, state="readonly")
        material_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        material_combo.bind('<<ComboboxSelected>>', self.on_material_selected)

        # Anyaginformációk megjelenítése
        self.material_info = tk.Text(material_frame, height=5, width=40)
        self.material_info.pack(padx=5, pady=5, fill=tk.X)
        scrollbar = ttk.Scrollbar(material_frame, orient="vertical", command=self.material_info.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.material_info.configure(yscrollcommand=scrollbar.set)

        # Sugár beviteli mezők
        radius_frame = ttk.LabelFrame(input_frame, text="Sugár beállítások", padding=5)
        radius_frame.pack(fill=tk.X, pady=2)
        
        # Sugártípus választó
        radius_type_frame = ttk.Frame(radius_frame)
        radius_type_frame.pack(fill=tk.X, pady=2)
        ttk.Label(radius_type_frame, text="Sugártípus:", width=20).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(radius_type_frame, text="Belső", variable=self.radius_type,
                       value="inner", command=self.toggle_radius_input).pack(side=tk.LEFT)
        ttk.Radiobutton(radius_type_frame, text="Semleges", variable=self.radius_type,
                       value="neutral", command=self.toggle_radius_input).pack(side=tk.LEFT)
        ttk.Radiobutton(radius_type_frame, text="Külső", variable=self.radius_type,
                       value="outer", command=self.toggle_radius_input).pack(side=tk.LEFT)

        radius_fields = [
            ("Belső sugár (mm):", self.inner_radius, "inner"),
            ("Semleges sugár (mm):", self.neutral_radius, "neutral"),
            ("Külső sugár (mm):", self.outer_radius, "outer")
        ]
        
        for label, var, key in radius_fields:
            frame = ttk.Frame(radius_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=label, width=20).pack(side=tk.LEFT, padx=5)
            entry = ttk.Entry(frame, textvariable=var, width=10)
            entry.pack(side=tk.LEFT)
            self.entries[key] = entry
            entry.configure(state='disabled')  # Alapértelmezetten minden inaktív
        
        # Geometria beállítások
        geometry_frame = ttk.LabelFrame(input_frame, text="Geometria beállítások", padding=5)
        geometry_frame.pack(fill=tk.X, pady=2)
        
        geometry_fields = [
            ("Lemezvastagság (mm):", self.thickness),
            ("K-faktor:", self.k_factor),
            ("Hajlítások száma:", self.segment_count),
            ("Hajlítási szög (°):", self.angle)
        ]
        
        for label, var in geometry_fields:
            frame = ttk.Frame(geometry_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=label, width=20).pack(side=tk.LEFT, padx=5)
            ttk.Entry(frame, textvariable=var, width=10).pack(side=tk.LEFT)
        
        # Egyenes szakaszok beállításai
        straight_frame = ttk.LabelFrame(input_frame, text="Egyenes szakaszok", padding=5)
        straight_frame.pack(fill=tk.X, pady=2)
        
        straight_fields = [
            ("Kezdő egyenes (mm):", self.start_length),
            ("Záró egyenes (mm):", self.end_length)
        ]
        
        for label, var in straight_fields:
            frame = ttk.Frame(straight_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=label, width=20).pack(side=tk.LEFT, padx=5)
            ttk.Entry(frame, textvariable=var, width=10).pack(side=tk.LEFT)

    def create_buttons(self, parent):
        """Gombok létrehozása"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Számítás",
                  command=self.calculate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Újra",
                  command=self.reset).pack(side=tk.LEFT, padx=5)

    def create_result_display(self, parent):
        """Eredmény megjelenítő létrehozása"""
        result_frame = ttk.LabelFrame(parent, text="Eredmények", padding=10)
        result_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.result_text = tk.Text(result_frame, height=12, width=60)
        self.result_text.pack(padx=5, pady=5)
        
        # Scrollbar az eredmény szöveghez
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.configure(yscrollcommand=scrollbar.set)

    def create_canvas(self, parent):
        """Canvas létrehozása"""
        canvas_frame = ttk.LabelFrame(parent, text="Vizualizáció", padding=10)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame,
                              width=CANVAS_WIDTH,
                              height=CANVAS_HEIGHT,
                              bg=COLORS['CANVAS_BG'])
        self.canvas.pack(padx=5, pady=5)
        
        # Drawing manager inicializálása
        self.drawing_manager = DrawingManager(self.canvas)
        
        # Koordinátarendszer rajzolása
        self.canvas.update()  # Várjuk meg, amíg a canvas mérete beáll
        self.drawing_manager.draw_coordinate_system()
        
        # Zoom és pan események beállítása
        self.setup_zoom_pan()

    def setup_zoom_pan(self):
        """Zoom és pan események beállítása"""
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        
        # Canvas eseménykezelők
        self.canvas.bind('<MouseWheel>', self.on_mousewheel)
        self.canvas.bind('<ButtonPress-1>', self.start_pan)
        self.canvas.bind('<B1-Motion>', self.pan)
        self.canvas.bind('<ButtonRelease-1>', self.stop_pan)
        
        # Scrollbar eseménykezelők az anyaginformációkhoz és eredményekhez
        def on_mousewheel(event, widget):
            if str(event.widget) == str(widget):
                widget.yview_scroll(int(-1*(event.delta/120)), "units")
            return "break"
        
        # Anyaginformációk scrollbar
        if hasattr(self, 'material_info'):
            self.material_info.bind('<MouseWheel>', 
                lambda e: on_mousewheel(e, self.material_info))
        
        # Eredmények scrollbar
        if hasattr(self, 'result_text'):
            self.result_text.bind('<MouseWheel>', 
                lambda e: on_mousewheel(e, self.result_text))

    def on_material_selected(self, event=None):
        """Anyag kiválasztásakor frissítjük az anyag információkat"""
        # Kiválasztott anyag kódjának kinyerése
        selected = self.material_var.get()
        material_code = selected.split(" - ")[0]
        
        # Anyag tulajdonságainak lekérése
        material = MATERIALS[material_code]
        
        # Információs szöveg összeállítása
        info_text = f"Anyag neve: {material['name']}\n"
        info_text += f"Típus: {material['type']}\n"
        info_text += f"Young modulus (E): {material['E']} MPa\n"
        info_text += f"Folyáshatár (Re): {material['Re']} MPa\n"
        info_text += f"Szakítószilárdság (Rm): {material['Rm']} MPa\n"
        info_text += f"Szakadási nyúlás (A80): {material['A80']}%\n"
        info_text += f"Poisson tényező: {material['poisson']}\n"
        info_text += f"K-tényező: {material['k_factor']}\n"
        info_text += f"Min. hajlítási sugár: {material['min_r']}×t\n"
        info_text += f"Visszarugózási tényező: {material['springback']}"
        
        # Text widget tartalmának frissítése
        self.material_info.config(state='normal')
        self.material_info.delete(1.0, tk.END)
        self.material_info.insert(1.0, info_text)
        self.material_info.config(state='disabled')
        
        # K-tényező frissítése
        self.k_factor.set(str(material['k_factor']))

    def toggle_radius_input(self):
        """Sugár típus váltásakor frissítjük az input mezőket"""
        # Input mezők tiltása/engedélyezése a kiválasztott sugártípus alapján
        self.entries['inner'].configure(state='disabled')
        self.entries['neutral'].configure(state='disabled')
        self.entries['outer'].configure(state='disabled')
        
        selected_type = self.radius_type.get()
        if selected_type in self.entries:
            self.entries[selected_type].configure(state='normal')
        
        # Ha van már érték beírva, számoljunk újra
        try:
            if (selected_type == "inner" and self.inner_radius.get() or
                selected_type == "neutral" and self.neutral_radius.get() or
                selected_type == "outer" and self.outer_radius.get()):
                self.calculate()
        except:
            pass  # Ha még nincs elegendő adat a számításhoz

    def calculate(self):
        """Számítások elvégzése és megjelenítése"""
        try:
            # Adatok beolvasása
            radius_type = self.radius_type.get()
            radius_value = getattr(self, f"{radius_type}_radius").get()
            thickness = float(self.thickness.get())
            k_factor = float(self.k_factor.get())
            segment_count = int(self.segment_count.get())
            total_angle = float(self.angle.get())
            start_length = float(self.start_length.get() or 0)
            end_length = float(self.end_length.get() or 0)

            # Sugarak számítása
            inner_radius, neutral_radius, outer_radius = calculate_radii(
                radius_type, radius_value, thickness, k_factor)
            
            # Eredmények megjelenítése
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, f"Belső sugár: {inner_radius:.2f} mm\n")
            self.result_text.insert(tk.END, f"Semleges sugár: {neutral_radius:.2f} mm\n")
            self.result_text.insert(tk.END, f"Külső sugár: {outer_radius:.2f} mm\n")
            
            # Visszarugózás számítása és megjelenítése
            selected_material = self.material_var.get()
            if selected_material in [f"{code} - {MATERIALS[code]['name']}" for code in MATERIALS.keys()]:
                code = selected_material.split(' - ')[0]
                springback = MATERIALS[code]['springback']
                springback_angle = total_angle * (1 - springback)
                self.result_text.insert(tk.END, f"\nVárható visszarugózás: {springback_angle:.1f}°\n")
            
            # A kiválasztott sugár meghatározása az ívhossz számításához
            selected_radius = {
                "inner": inner_radius,
                "neutral": neutral_radius,
                "outer": outer_radius
            }[radius_type]
            
            # Ívhossz és teljes hossz számítása
            arc_length = selected_radius * math.radians(total_angle)
            total_length = start_length + arc_length + end_length
            
            self.result_text.insert(tk.END, f"Ívhossz: {arc_length:.2f} mm\n")
            self.result_text.insert(tk.END, f"Teljes hossz: {total_length:.2f} mm\n")
            
            # Canvas törlése és rajzolás
            self.drawing_manager.clear_canvas()
            self.draw_bending(inner_radius, neutral_radius, outer_radius,
                            total_angle, segment_count, start_length, end_length)
                            
        except ValueError as e:
            self.show_error("Hiba: Kérem ellenőrizze a bevitt adatokat!")
        except Exception as e:
            self.show_error(f"Hiba történt: {str(e)}")

    def draw_bending(self, inner_radius, neutral_radius, outer_radius,
                    total_angle, segment_count, start_length, end_length):
        """Hajlítás rajzolása"""
        # Canvas méretezése
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Középpont és skála számítása
        center_x = canvas_width / 2
        center_y = canvas_height / 2
        scale = min(canvas_width, canvas_height) / (3 * outer_radius) * self.zoom_factor
        
        # Hajlítási szög számítása
        bend_angle = total_angle / segment_count  # Egy hajlítás szöge
        complementary_angle = 180 - bend_angle    # Mellékszög
        
        # Ívek rajzolása
        for radius, color, dash_pattern in [
            (inner_radius, COLORS['INNER_LINE_COLOR'], None),
            (neutral_radius, COLORS['NEUTRAL_LINE_COLOR'], (2, 2)),
            (outer_radius, COLORS['OUTER_LINE_COLOR'], None)
        ]:
            scaled_radius = radius * scale
            self.drawing_manager.draw_arc(
                center_x, center_y,
                scaled_radius, -total_angle,
                color, dash_pattern
            )
        
        # Hajlítási pontok és húrok rajzolása (mindig a belső sugáron)
        points = []
        angles = []  # Szögek tárolása a húrhossz számításhoz
        
        # Hajlítási pontok generálása
        for i in range(segment_count):
            # A szög számítása az i. ponthoz (egyenletes eloszlás)
            current_angle = total_angle * i / (segment_count - 1)
            angle_rad = math.radians(90 - current_angle)
            angles.append(current_angle)
            
            # Pont koordináták számítása (mindig a belső sugárral)
            x = center_x + inner_radius * scale * math.cos(angle_rad)
            y = center_y - inner_radius * scale * math.sin(angle_rad)
            points.append((x, y))
            
            # Pont rajzolása
            self.drawing_manager.draw_point(x, y)
            
            # Sugár rajzolása
            self.drawing_manager.draw_radius_line(center_x, center_y, x, y)
            
            # Mellékszög megjelenítése minden hajlítási pontnál
            self.drawing_manager.draw_complementary_angle(
                center_x, center_y, x, y,
                complementary_angle, outer_radius, scale
            )
        
        # Húrok rajzolása (segment_count - 1 darab húr)
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            
            # Húr rajzolása vastag szaggatott vonallal
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=COLORS['CHORD_LINE_COLOR'],
                dash=(5, 5),
                width=2
            )
            
            # Húrhossz számítása két pont között
            angle_diff = abs(angles[i+1] - angles[i])  # Szögkülönbség radiánban
            chord_length = 2 * inner_radius * abs(math.sin(math.radians(angle_diff/2)))
            
            # Húrhossz megjelenítése
            self.drawing_manager.draw_chord_length(x1, y1, x2, y2, chord_length)
        
        # Kezdő és záró egyenes szakaszok rajzolása (fekete színnel)
        if points and start_length > 0:
            # Kezdő pont
            angle = math.radians(90)  # Függőleges irány
            start_x = points[0][0] - (start_length * scale * math.sin(angle))
            start_y = points[0][1] - (start_length * scale * math.cos(angle))
            self.drawing_manager.draw_straight_line(
                start_x, start_y,
                points[0][0], points[0][1]
            )
        
        if points and end_length > 0:
            # Záró egyenes - mint egy következő húr
            last_point = points[-1]
            # Következő szegmens szöge
            next_angle = math.radians(90 - total_angle)
            
            # A záróegyenes végpontja
            end_x = last_point[0] + end_length * scale * math.cos(next_angle - math.pi/2)
            end_y = last_point[1] - end_length * scale * math.sin(next_angle - math.pi/2)
            
            # Záróegyenes rajzolása
            self.drawing_manager.draw_straight_line(
                last_point[0], last_point[1],
                end_x, end_y
            )

    def show_results(self, inner_radius, neutral_radius, outer_radius):
        """Eredmények megjelenítése"""
        result = f"Számítás eredménye:\n\n"
        result += f"Belső sugár: {inner_radius:.2f} mm\n"
        result += f"Semleges sugár: {neutral_radius:.2f} mm\n"
        result += f"Külső sugár: {outer_radius:.2f} mm\n"
        
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', result)

    def show_error(self, message):
        """Hibaüzenet megjelenítése"""
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', f"HIBA: {message}")

    def reset(self):
        """Mezők alaphelyzetbe állítása"""
        for var in [self.inner_radius, self.neutral_radius, self.outer_radius,
                   self.thickness, self.k_factor, self.segment_count,
                   self.angle, self.start_length, self.end_length]:
            var.set("")
        
        self.material_var.set("DC04 (1.0338)")
        self.radius_type.set("inner")
        self.toggle_radius_input()
        self.drawing_manager.clear_canvas()
        self.result_text.delete('1.0', tk.END)

    def on_mousewheel(self, event):
        """Nagyítás/kicsinyítés kezelése"""
        if str(event.widget) == str(self.canvas):
            # Csak akkor zoomolunk, ha a canvas felett van az egér
            if event.delta > 0:
                self.zoom_factor *= 1.1
            else:
                self.zoom_factor /= 1.1
            self.calculate()  # Újrarajzolás az új zoom faktorral
            return "break"

    def start_pan(self, event):
        """Eltolás kezdése"""
        self.canvas.scan_mark(event.x, event.y)

    def pan(self, event):
        """Eltolás végrehajtása"""
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def stop_pan(self, event):
        """Eltolás befejezése"""
        pass
