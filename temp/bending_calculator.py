import tkinter as tk
from tkinter import ttk
import math
from material_database import MATERIALS

class BendingCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Lemez Hajlítás Kalkulátor")
        
        # Teljes képernyő mód beállítása
        self.root.state('zoomed')  # Windows-specifikus teljes képernyő mód
        
        # Főablak minimum méretének beállítása
        self.root.minsize(1000, 600)
        
        # Fő frame létrehozása scrollbarral
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas és scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        # Scrollable frame
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Canvas ablak létrehozása
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack elrendezés
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Változók létrehozása
        self.radius_type = tk.StringVar(value="inner")
        self.inner_radius = tk.StringVar()
        self.neutral_radius = tk.StringVar()
        self.outer_radius = tk.StringVar()
        self.thickness = tk.StringVar()
        self.k_factor = tk.StringVar()
        self.segment_count = tk.StringVar()
        self.angle = tk.StringVar()
        self.start_length = tk.StringVar()
        self.end_length = tk.StringVar()
        self.material_var = tk.StringVar()
        
        # Bal oldali panel az inputoknak
        left_panel = ttk.Frame(scrollable_frame)
        left_panel.grid(row=0, column=0, sticky="ns", padx=(10, 10))
        
        # Jobb oldali panel a canvasnak és eredményeknek
        right_panel = ttk.Frame(scrollable_frame)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 10))
        
        # Input mezők kerete
        input_frame = ttk.LabelFrame(left_panel, text="Adatok", padding=10)
        input_frame.grid(row=0, column=0, sticky="new")
        
        # Anyagválasztó keret
        material_frame = ttk.LabelFrame(input_frame, text="Anyagválasztás", padding=5)
        material_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Anyagválasztó legördülő lista
        self.material_combo = ttk.Combobox(material_frame, 
                                         textvariable=self.material_var,
                                         values=list(MATERIALS.keys()),
                                         state="readonly",
                                         width=30)
        self.material_combo.grid(row=0, column=0, sticky="ew", padx=5)
        self.material_combo.bind('<<ComboboxSelected>>', self.on_material_selected)
        
        # Anyag tulajdonságok megjelenítése
        self.material_info = tk.Text(material_frame, height=4, width=40)
        self.material_info.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        # Sugár típus választó
        radius_frame = ttk.LabelFrame(input_frame, text="Sugár típusa", padding=5)
        radius_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        
        ttk.Radiobutton(radius_frame, text="Belső sugár", variable=self.radius_type,
                       value="inner", command=self.toggle_radius_input).grid(row=0, column=0, sticky="w", padx=5)
        ttk.Radiobutton(radius_frame, text="Semleges sugár", variable=self.radius_type,
                       value="neutral", command=self.toggle_radius_input).grid(row=0, column=1, sticky="w", padx=5)
        ttk.Radiobutton(radius_frame, text="Külső sugár", variable=self.radius_type,
                       value="outer", command=self.toggle_radius_input).grid(row=0, column=2, sticky="w", padx=5)
        
        # Input mezők
        self.input_fields_frame = ttk.Frame(input_frame, padding=5)
        self.input_fields_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        
        # Input mezők létrehozása
        self.inner_entry = self.create_input_field(self.input_fields_frame, "Belső sugár (mm):", self.inner_radius, 0, "inner")
        self.neutral_entry = self.create_input_field(self.input_fields_frame, "Semleges sugár (mm):", self.neutral_radius, 1, "neutral")
        self.outer_entry = self.create_input_field(self.input_fields_frame, "Külső sugár (mm):", self.outer_radius, 2, "outer")
        self.create_input_field(self.input_fields_frame, "Lemezvastagság (mm):", self.thickness, 3)
        self.create_input_field(self.input_fields_frame, "K-faktor:", self.k_factor, 4)
        self.create_input_field(self.input_fields_frame, "Hajlítások száma:", self.segment_count, 5)
        self.create_input_field(self.input_fields_frame, "Teljes szög (°):", self.angle, 6)
        self.create_input_field(self.input_fields_frame, "Kezdő egyenes (mm):", self.start_length, 7)
        self.create_input_field(self.input_fields_frame, "Záró egyenes (mm):", self.end_length, 8)
        
        # Gombok
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Számítás", command=self.calculate).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Újra", command=self.reset).grid(row=0, column=1, padx=5)
        
        # Eredmények szövegdoboz - bal oldalt lent
        result_frame = ttk.LabelFrame(left_panel, text="Eredmények", padding=10)
        result_frame.grid(row=1, column=0, sticky="nw", pady=(10, 0))
        self.result_text = tk.Text(result_frame, height=12, width=60)  
        self.result_text.grid(row=0, column=0, padx=5, pady=5)
        
        # Scrollbar hozzáadása az eredmények szövegdobozhoz
        result_scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        result_scrollbar.grid(row=0, column=1, sticky="ns")
        self.result_text.configure(yscrollcommand=result_scrollbar.set)
        
        # Canvas keret - jobb felső sarok
        canvas_frame = ttk.LabelFrame(right_panel, text="Vizualizáció", padding=10)
        canvas_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Canvas nagyobb mérettel
        self.canvas = tk.Canvas(canvas_frame, width=900, height=700, bg='white')
        self.canvas.grid(row=0, column=0, padx=5, pady=5)
        
        # Zoom és pan változók
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.last_x = 0
        self.last_y = 0
        self.panning = False
        
        # Zoom és pan eseménykezelők hozzáadása csak a canvashez
        self.canvas.bind('<MouseWheel>', self.on_mousewheel)  # Nagyítás a canvas felett
        self.canvas.bind('<ButtonPress-1>', self.start_pan)
        self.canvas.bind('<B1-Motion>', self.pan)
        self.canvas.bind('<ButtonRelease-1>', self.stop_pan)
        
        # Input mezők szélességének beállítása
        for child in self.input_fields_frame.winfo_children():
            if isinstance(child, ttk.Entry):
                child.config(width=15)
        
        # Egérgörgő esemény kezelése a scrollozáshoz (csak a fő canvas-en)
        def scroll_handler(event):
            if str(event.widget) != str(self.canvas):
                canvas.yview_scroll(-1*(event.delta//120), "units")
        
        canvas.bind_all("<MouseWheel>", scroll_handler)
        
        # Kezdeti állapot beállítása
        self.toggle_radius_input()
        
    def create_input_field(self, parent, label, variable, row, name=None):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=2)
        entry = ttk.Entry(parent, textvariable=variable)
        if name:
            entry.name = name
        entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        return entry
    
    def toggle_radius_input(self):
        # Input mezők tiltása/engedélyezése a kiválasztott sugártípus alapján
        self.inner_entry.configure(state='disabled')
        self.neutral_entry.configure(state='disabled')
        self.outer_entry.configure(state='disabled')
        
        if self.radius_type.get() == "inner":
            self.inner_entry.configure(state='normal')
        elif self.radius_type.get() == "neutral":
            self.neutral_entry.configure(state='normal')
        else:  # outer
            self.outer_entry.configure(state='normal')
            
        # Ha van már érték beírva, számoljunk újra
        try:
            if (self.radius_type.get() == "inner" and self.inner_radius.get() or
                self.radius_type.get() == "neutral" and self.neutral_radius.get() or
                self.radius_type.get() == "outer" and self.outer_radius.get()):
                self.calculate()
        except:
            pass  # Ha még nincs elegendő adat a számításhoz, ne csináljunk semmit
    
    def reset(self):
        self.inner_radius.set("")
        self.neutral_radius.set("")
        self.outer_radius.set("")
        self.thickness.set("")
        self.k_factor.set("")
        self.segment_count.set("")
        self.angle.set("")
        self.start_length.set("")
        self.end_length.set("")
        self.result_text.delete(1.0, tk.END)
        self.canvas.delete("all")
        self.draw_coordinate_system()
        
    def draw_coordinate_system(self):
        # Koordinátarendszer rajzolása
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Vízszintes vonal
        self.canvas.create_line(50, height/2, width-50, height/2, fill='#ccc')
        # Függőleges vonal
        self.canvas.create_line(width/2, 50, width/2, height-50, fill='#ccc')
        
    def calculate(self):
        try:
            thickness = float(self.thickness.get())
            k_factor = float(self.k_factor.get()) if self.k_factor.get() else 0.35
            total_angle = float(self.angle.get())
            segment_count = int(self.segment_count.get()) if self.segment_count.get() else 1
            start_length = float(self.start_length.get()) if self.start_length.get() else 0
            end_length = float(self.end_length.get()) if self.end_length.get() else 0
            
            # Sugarak számítása a kiválasztott típus alapján
            if self.radius_type.get() == "inner":
                inner_radius = float(self.inner_radius.get())
                neutral_radius = inner_radius + thickness * k_factor
                outer_radius = inner_radius + thickness
            elif self.radius_type.get() == "neutral":
                neutral_radius = float(self.neutral_radius.get())
                inner_radius = neutral_radius - thickness * k_factor
                outer_radius = neutral_radius + thickness * (1 - k_factor)  # Javítva
            else:  # outer
                outer_radius = float(self.outer_radius.get())
                inner_radius = outer_radius - thickness
                neutral_radius = inner_radius + thickness * k_factor
                
            # Anyag tulajdonságok lekérése
            if self.material_var.get():
                material = MATERIALS[self.material_var.get()]
                springback = material['springback']
                min_r_factor = material['min_r']
            else:
                springback = 1.0
                min_r_factor = 0.5
            
            # Minimális hajlítási sugár ellenőrzése
            min_radius = thickness * min_r_factor
            
            # Eredmények megjelenítése csak az eredmények mezőben
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Belső sugár (Ri): {inner_radius:.2f} mm\n")
            self.result_text.insert(tk.END, f"Semleges sugár (Rs): {neutral_radius:.2f} mm\n")
            self.result_text.insert(tk.END, f"Külső sugár (Rk): {outer_radius:.2f} mm\n\n")
            
            # Ívhosszak számítása
            inner_arc = inner_radius * math.radians(total_angle)
            neutral_arc = neutral_radius * math.radians(total_angle)
            outer_arc = outer_radius * math.radians(total_angle)
            
            self.result_text.insert(tk.END, f"Belső ív (zömülés): {inner_arc:.2f} mm\n")
            self.result_text.insert(tk.END, f"Semleges ív: {neutral_arc:.2f} mm\n")
            self.result_text.insert(tk.END, f"Külső ív (nyúlás): {outer_arc:.2f} mm\n\n")

            # Húrok összegének számítása
            total_chords = 0
            for i in range(segment_count - 1):  # Minden húr között
                angle1 = math.radians(90 - total_angle * (i / (segment_count - 1)))
                angle2 = math.radians(90 - total_angle * ((i + 1) / (segment_count - 1)))
                
                x1 = inner_radius * math.cos(angle1)
                y1 = inner_radius * math.sin(angle1)
                x2 = inner_radius * math.cos(angle2)
                y2 = inner_radius * math.sin(angle2)
                
                chord_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                total_chords += chord_length

            # Összehasonlítás megjelenítése
            self.result_text.insert(tk.END, f"\nÖsszehasonlítás a belső íven:\n")
            self.result_text.insert(tk.END, f"Belső ívhossz: {inner_arc:.2f} mm\n")
            self.result_text.insert(tk.END, f"Húrok összege: {total_chords:.2f} mm\n")
            self.result_text.insert(tk.END, f"Különbség: {inner_arc - total_chords:.2f} mm\n")
            self.result_text.insert(tk.END, f"Eltérés: {((inner_arc - total_chords) / inner_arc * 100):.1f}%\n")
            
            # Alakváltozások
            inner_strain = ((neutral_arc - inner_arc) / neutral_arc) * 100
            outer_strain = ((outer_arc - neutral_arc) / neutral_arc) * 100
            
            self.result_text.insert(tk.END, f"Belső szálon zömülés: {inner_strain:.1f}%\n")
            self.result_text.insert(tk.END, f"Külső szálon nyúlás: {outer_strain:.1f}%\n")
            
            if self.material_var.get():
                material = MATERIALS[self.material_var.get()]
                if outer_strain > material['A80']:
                    self.result_text.insert(tk.END, "\nFigyelem: A számított nyúlás meghaladja az anyag szakadási nyúlását!")
                
                # Visszarugózás számítása
                springback_angle = total_angle * (1 - springback)
                self.result_text.insert(tk.END, f"\nVárható visszarugózás: {springback_angle:.1f}°")
            
            # A kiválasztott sugár meghatározása az ívhossz számításához
            if self.radius_type.get() == "inner":
                selected_radius = inner_radius
            elif self.radius_type.get() == "neutral":
                selected_radius = neutral_radius
            else:  # outer
                selected_radius = outer_radius
                
            self.result_text.insert(tk.END, f"Ívhossz: {selected_radius * math.radians(total_angle):.2f} mm\n")
            self.result_text.insert(tk.END, f"Teljes hossz: {start_length + selected_radius * math.radians(total_angle) + end_length:.2f} mm\n")
            
            # Vizualizáció
            self.draw_bending(inner_radius, neutral_radius, outer_radius,
                            total_angle, segment_count, start_length, end_length)
            
        except ValueError as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Hiba: Kérem ellenőrizze a bevitt adatokat!")
            
    def draw_bending(self, inner_radius, neutral_radius, outer_radius,
                    total_angle, segment_count, start_length, end_length):
        # Canvas törlése
        self.canvas.delete("all")
        
        # A kiválasztott sugár a rádiógomb alapján
        if self.radius_type.get() == "inner":
            selected_radius = inner_radius
        elif self.radius_type.get() == "neutral":
            selected_radius = neutral_radius
        else:  # outer
            selected_radius = outer_radius
        
        # Ívhossz számítása (körív hossza = sugár * szög radiánban)
        arc_length = selected_radius * math.radians(total_angle)
        
        # Teljes hossz = kezdő szakasz + ívhossz + záró szakasz
        total_length = start_length + arc_length + end_length
        
        # Méretek és skála számítása
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width / 2 + self.pan_x
        center_y = height / 2 + self.pan_y
        
        # Teljes méret számítása a kiválasztott sugárral
        arc_width = 2 * selected_radius * math.sin(math.radians(total_angle/2))
        arc_height = selected_radius * (1 - math.cos(math.radians(total_angle/2)))
        total_width = arc_width + start_length + end_length
        total_height = max(arc_height * 2, selected_radius * 2)
        
        # Skála számítása
        padding = 50
        scale_x = (width - 2 * padding) / total_width
        scale_y = (height - 2 * padding) / total_height
        scale = min(scale_x, scale_y) * self.zoom_factor
        
        # Teljes szög korrekciója (180-szög)
        total_angle = 180 - total_angle
        
        # A hajlítási szög a teljes szög osztva a hajlítások számával
        bend_angle = total_angle / segment_count
        # A kiegészítő szög: 180° - hajlítási szög
        complementary_angle = 180 - bend_angle

        # Függőleges eltolás számítása
        vertical_offset = (arc_height * scale) / 2
        adjusted_center_y = center_y + vertical_offset

        # Koordinátatengelyek rajzolása
        # X tengely
        self.canvas.create_line(0, adjusted_center_y, width, adjusted_center_y, 
                              fill='gray', arrow=tk.LAST, dash=(4, 2))
        self.canvas.create_text(width-20, adjusted_center_y-10, text="X", fill='gray')
        
        # Y tengely
        self.canvas.create_line(center_x, 0, center_x, height,
                              fill='gray', arrow=tk.LAST, dash=(4, 2))
        self.canvas.create_text(center_x+10, 20, text="Y", fill='gray')
        
        # Origó jelölése
        self.canvas.create_oval(center_x-5, adjusted_center_y-5,
                              center_x+5, adjusted_center_y+5,
                              fill='gray')
        self.canvas.create_text(center_x-15, adjusted_center_y+15,
                              text="O", fill='gray')
        
        # Ívek rajzolása
        start_angle = 90  # Kezdőpont az X tengelyen (90 fok)
        end_angle = start_angle - total_angle  # Az óramutató járásával megegyező irányba
        
        # Ívek rajzolása
        for radius, color in [(inner_radius, 'red'), (neutral_radius, 'green'), (outer_radius, 'blue')]:
            scaled_radius = radius * scale
            # Szaggatott vonal a semleges szálhoz
            dash_pattern = (5, 5) if radius == neutral_radius else None
            
            # Ív rajzolása
            self.canvas.create_arc(
                center_x - scaled_radius, adjusted_center_y - scaled_radius,
                center_x + scaled_radius, adjusted_center_y + scaled_radius,
                start=90, extent=-total_angle,
                style="arc", width=2, outline=color, dash=dash_pattern
            )
        
        # Pontok és húrok rajzolása
        for i in range(segment_count):  # Pontosan annyi pont, ahány hajlítás
            # A progress most 0-tól 1-ig megy
            progress = i / (segment_count - 1) if segment_count > 1 else 0
            angle = math.radians(90 - total_angle * progress)  # 90 fokról indulva
            
            # Hajlítási pont koordináták a kiválasztott sugárral
            x = center_x + selected_radius * scale * math.cos(angle)
            y = adjusted_center_y - selected_radius * scale * math.sin(angle)  # Negatív sin a helyes irányhoz
            
            # Pont rajzolása - minden pont hajlítási pont
            self.canvas.create_oval(
                x - 2, y - 2,
                x + 2, y + 2,
                fill='red'
            )
            
            # Sugár rajzolása a középponttól a hajlítási pontig és kiegészítő szög megjelenítése
            self.canvas.create_line(
                center_x, adjusted_center_y,
                x, y,
                fill='green', width=1, dash=(2, 2)  # szaggatott zöld vonal
            )
            
            # Kiegészítő szög megjelenítése a sugár mentén
            if i < segment_count:  # Most már az i == 0 esetben is megjelenik
                # A hajlítási szög a teljes szög osztva a hajlítások számával
                bend_angle = total_angle / segment_count
                # A kiegészítő szög: 180° - hajlítási szög
                complementary_angle = 180 - bend_angle
                
                # A sugár irányának kiszámítása
                dx = x - center_x
                dy = y - adjusted_center_y
                angle = math.atan2(dy, dx)
                
                # Szöveg pozíciója a sugár mentén, külső köríven kívül 10 egységgel
                text_distance = (outer_radius * scale) + (10 * scale)
                text_x = center_x + text_distance * math.cos(angle)
                text_y = adjusted_center_y + text_distance * math.sin(angle)
                
                # Kiegészítő szög kiírása
                self.canvas.create_text(
                    text_x, text_y,
                    text=f"{complementary_angle:.1f}°",
                    fill='blue'
                )
            
            # Első és utolsó pont mentése a kezdő és záró egyenesekhez
            if i == 0:
                first_point = (x, y)
            elif i == segment_count - 1:
                last_point = (x, y)
            
            # Húr rajzolása és méretének megjelenítése
            if i < segment_count - 1:  # Egy húrral kevesebb mint hajlítási pont
                next_progress = (i + 1) / (segment_count - 1) if segment_count > 1 else 0
                next_angle = math.radians(90 - total_angle * next_progress)
                next_x = center_x + selected_radius * scale * math.cos(next_angle)
                next_y = adjusted_center_y - selected_radius * scale * math.sin(next_angle)
                
                # Húr rajzolása
                self.canvas.create_line(x, y, next_x, next_y,
                                     fill='orange', dash=(2, 2))
                
                # Húr hosszának számítása a geometriai képlettel
                angle_between = total_angle / (segment_count - 1)  # Két pont közötti szög
                chord_length = 2 * inner_radius * math.sin(math.radians(angle_between/2))
                
                # Húr méretének kiírása a belső körív belső részén
                mid_angle = (angle + next_angle) / 2
                text_radius = inner_radius * 0.8  # A belső sugár 80%-ánál
                text_x = center_x + text_radius * scale * math.cos(mid_angle)
                text_y = adjusted_center_y - text_radius * scale * math.sin(mid_angle)
                
                self.canvas.create_text(
                    text_x, text_y,
                    text=f"{chord_length:.1f} mm",
                    fill='orange'
                )
        
        # Kezdő és záró egyenes szakaszok rajzolása
        if first_point and last_point and segment_count > 1:
            # Kezdő egyenes - vízszintesen indul
            if start_length > 0:
                start_x = first_point[0] - start_length * scale
                self.canvas.create_line(
                    start_x, first_point[1],
                    first_point[0], first_point[1],
                    fill='black', width=2
                )
                # Kezdőegyenes végpontjainak jelölése
                self.canvas.create_oval(
                    start_x - 3, first_point[1] - 3,
                    start_x + 3, first_point[1] + 3,
                    fill='red', outline='red'
                )
                self.canvas.create_oval(
                    first_point[0] - 3, first_point[1] - 3,
                    first_point[0] + 3, first_point[1] + 3,
                    fill='red', outline='red'
                )
            
            # Záró egyenes - mint egy következő húr, a hajlítási pontok számával elosztott szöggel
            if end_length > 0:
                # Következő szegmens szöge (mint egy következő húrnál)
                next_progress = segment_count / (segment_count)  # most 1.0
                next_angle = math.radians(90 - total_angle * next_progress)
                
                # A záróegyenes végpontja (ugyanúgy mint a húroknál)
                end_x = last_point[0] + end_length * scale * math.cos(next_angle - math.pi/2)
                end_y = last_point[1] - end_length * scale * math.sin(next_angle - math.pi/2)
                
                # Záróegyenes rajzolása
                self.canvas.create_line(
                    last_point[0], last_point[1],
                    end_x, end_y,
                    fill='black', width=2
                )
                
                # Végpontok jelölése
                self.canvas.create_oval(
                    last_point[0] - 3, last_point[1] - 3,
                    last_point[0] + 3, last_point[1] + 3,
                    fill='red', outline='red'
                )
                self.canvas.create_oval(
                    end_x - 3, end_y - 3,
                    end_x + 3, end_y + 3,
                    fill='red', outline='red'
                )
    
    def on_mousewheel(self, event):
        # Zoom faktor módosítása az egér görgő alapján
        if event.delta > 0:
            self.zoom_factor *= 1.1
        else:
            self.zoom_factor /= 1.1
        
        # Újrarajzolás az új zoom faktorral
        self.calculate()
    
    def start_pan(self, event):
        self.panning = True
        self.last_x = event.x
        self.last_y = event.y
        
    def stop_pan(self, event):
        self.panning = False
        
    def pan(self, event):
        if self.panning:
            # Az eltolás kiszámítása
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            
            # Pan értékek frissítése
            self.pan_x += dx
            self.pan_y += dy
            
            # Utolsó pozíció mentése
            self.last_x = event.x
            self.last_y = event.y
            
            # Újrarajzolás az új pan értékekkel
            self.calculate()
    
    def on_material_selected(self, event=None):
        # Kiválasztott anyag adatainak betöltése
        material = MATERIALS[self.material_var.get()]
        
        # Anyag információk megjelenítése
        self.material_info.delete(1.0, tk.END)
        self.material_info.insert(tk.END, 
            f"{material['name']}\n"
            f"Folyáshatár: {material['Re']} MPa\n"
            f"Szakítószilárdság: {material['Rm']} MPa\n"
            f"Nyúlás: {material['A80']}%")
        
        # K-faktor beállítása az anyag alapján
        self.k_factor.set(str(material['k_factor']))
        
        # Ha van már elegendő adat, számoljunk újra
        try:
            self.calculate()
        except:
            pass

def main():
    root = tk.Tk()
    app = BendingCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
