import math

def calculate_radii(radius_type, radius_value, thickness, k_factor):
    """Sugarak számítása a megadott típus alapján"""
    if radius_type == "inner":
        inner_radius = float(radius_value)
        neutral_radius = inner_radius + (thickness * k_factor)
        outer_radius = inner_radius + thickness
    elif radius_type == "neutral":
        neutral_radius = float(radius_value)
        inner_radius = neutral_radius - (thickness * k_factor)
        outer_radius = inner_radius + thickness
    else:  # outer
        outer_radius = float(radius_value)
        inner_radius = outer_radius - thickness
        neutral_radius = inner_radius + (thickness * k_factor)
    
    return inner_radius, neutral_radius, outer_radius

def calculate_bend_angles(total_angle, segment_count):
    """Hajlítási szögek számítása"""
    # A hajlítási szög a teljes szög osztva a hajlítások számával
    bend_angle = total_angle / segment_count
    # A mellékszög 180° - hajlítási szög
    complementary_angle = 180 - bend_angle
    return bend_angle, complementary_angle

def calculate_chord_length(point1, point2, scale):
    """Húrhossz számítása két pont között (valós méretben)"""
    # Visszaállítjuk a valós koordinátákat a skálázásból
    real_x1, real_y1 = point1[0] / scale, point1[1] / scale
    real_x2, real_y2 = point2[0] / scale, point2[1] / scale
    # Húrhossz számítása
    dx = real_x2 - real_x1
    dy = real_y2 - real_y1
    return math.sqrt(dx*dx + dy*dy)

def calculate_point_coordinates(center_x, center_y, radius, angle, scale):
    """Pont koordinátáinak számítása"""
    x = center_x + (radius * scale) * math.cos(angle)
    y = center_y - (radius * scale) * math.sin(angle)
    return x, y

def calculate_text_position(center_x, center_y, radius, angle, offset, scale):
    """Szöveg pozíciójának számítása"""
    text_distance = (radius * scale) + (offset * scale)
    text_x = center_x + text_distance * math.cos(angle)
    text_y = center_y + text_distance * math.sin(angle)
    return text_x, text_y
