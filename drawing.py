import math
from config import COLORS, POINT_SIZE, DASH_PATTERN, TEXT_OFFSET, FONT_SETTINGS
import tkinter as tk

class DrawingManager:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw_point(self, x, y):
        """Pont rajzolása"""
        self.canvas.create_oval(
            x - POINT_SIZE, y - POINT_SIZE,
            x + POINT_SIZE, y + POINT_SIZE,
            fill=COLORS['POINT_COLOR']
        )

    def draw_radius_line(self, center_x, center_y, x, y):
        """Sugár rajzolása"""
        self.canvas.create_line(
            center_x, center_y, x, y,
            fill=COLORS['RADIUS_LINE_COLOR'],
            width=1,
            dash=DASH_PATTERN
        )

    def draw_chord_length(self, x1, y1, x2, y2, length, offset=10):
        """Húrhossz megjelenítése"""
        # A húr középpontja
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        # A húr iránya
        dx = x2 - x1
        dy = y2 - y1
        screen_length = math.sqrt(dx*dx + dy*dy)  # Csak az offset irányához kell
        
        if screen_length != 0:
            # Merőleges vektor a húrra (befelé mutat)
            nx = -dy / screen_length
            ny = dx / screen_length
            
            # A szöveg pozíciója
            text_x = mid_x + nx * offset
            text_y = mid_y + ny * offset
            
            self.canvas.create_text(
                text_x, text_y,
                text=f"{length:.1f} mm",
                fill=COLORS['CHORD_TEXT_COLOR']
            )

    def draw_complementary_angle(self, center_x, center_y, x, y, angle, outer_radius, scale):
        """Kiegészítő szög megjelenítése"""
        # A sugár irányának kiszámítása
        dx = x - center_x
        dy = y - center_y
        direction = math.atan2(dy, dx)
        
        # Szöveg pozíciója
        text_distance = (outer_radius * scale) + (TEXT_OFFSET * scale)
        text_x = center_x + text_distance * math.cos(direction)
        text_y = center_y + text_distance * math.sin(direction)
        
        self.canvas.create_text(
            text_x, text_y,
            text=f"{angle:.1f}°",
            fill=COLORS['ANGLE_TEXT_COLOR'],
            font=FONT_SETTINGS
        )

    def draw_straight_line(self, start_x, start_y, end_x, end_y):
        """Egyenes szakasz rajzolása"""
        self.canvas.create_line(
            start_x, start_y,
            end_x, end_y,
            fill='black',  # Fekete szín a kezdő és záró egyenesekhez
            width=1
        )

    def draw_arc(self, center_x, center_y, radius, angle, color, dash_pattern=None):
        """Ív rajzolása"""
        # Az ív kezdő és végpontjainak kiszámítása
        start_angle = 90  # Felfelé indulunk
        end_angle = 90 + angle  # Az óramutató járásával megegyező irányba
        
        # Az ív rajzolása
        x0 = center_x - radius
        y0 = center_y - radius
        x1 = center_x + radius
        y1 = center_y + radius
        
        self.canvas.create_arc(
            x0, y0, x1, y1,
            start=start_angle,
            extent=angle,
            style="arc",
            outline=color,
            dash=dash_pattern
        )

    def draw_coordinate_system(self):
        """Koordinátarendszer rajzolása"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width / 2
        center_y = height / 2
        
        # X tengely
        self.canvas.create_line(0, center_y, width, center_y, 
                              fill='gray', arrow=tk.LAST)
        # Y tengely
        self.canvas.create_line(center_x, height, center_x, 0, 
                              fill='gray', arrow=tk.LAST)
        
        # Tengelyek feliratozása
        self.canvas.create_text(width - 20, center_y - 10, text="X", fill='gray')
        self.canvas.create_text(center_x + 10, 20, text="Y", fill='gray')
        
        # Origó jelölése
        self.canvas.create_text(center_x - 10, center_y + 10, text="O", fill='gray')

    def clear_canvas(self):
        """Canvas törlése"""
        self.canvas.delete("all")
        self.draw_coordinate_system()
