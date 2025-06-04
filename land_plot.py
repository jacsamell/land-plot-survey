import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import math

def normalize_bearing(bearing):
    """Normalize bearing to 0-360 range"""
    while bearing >= 360:
        bearing -= 360
    while bearing < 0:
        bearing += 360
    return bearing

def bearing_to_radians(bearing_deg):
    """Convert bearing to radians for calculations"""
    # Bearing is measured clockwise from north
    # Convert to standard math angle (counter-clockwise from east)
    angle_deg = 90 - bearing_deg
    if angle_deg < 0:
        angle_deg += 360
    return math.radians(angle_deg)

def feet_inches_to_feet(feet, inches=0):
    """Convert feet and inches to decimal feet"""
    return feet + inches / 12.0

print("Plot 7 - Step by Step Survey")
print("=" * 40)

# Start simple - build the traverse step by step
vertices = [(0.0, 0.0)]
current_x, current_y = 0.0, 0.0

# Side 1: 60' at bearing 340°6' magnetic (354°56' true back-azimuth, 174°56' forward)
length1 = 60.0
magnetic_bearing1 = 340 + 6/60  # 340°6'
magnetic_declination = 14 + 50/60  # 14°50'
back_azimuth = normalize_bearing(magnetic_bearing1 + magnetic_declination)  # 354°56' true
bearing1 = normalize_bearing(back_azimuth + 180)  # 174°56' true (actual direction)
angle1_rad = bearing_to_radians(bearing1)
dx1 = length1 * math.cos(angle1_rad)
dy1 = length1 * math.sin(angle1_rad)
current_x += dx1
current_y += dy1
vertices.append((current_x, current_y))
print(f"Side 1: {length1}' @ {bearing1:.1f}° (174°56' true from 340°6' mag back-azimuth) -> Point ({current_x:.1f}, {current_y:.1f})")

current_bearing = bearing1

# Side 2: 87'1" with internal angle (180-67°50') = 112°10'
length2 = feet_inches_to_feet(87, 1)
internal_angle2 = 180 - 67 - 50/60  # 112°10' = 112.167°
# Calculate next bearing: current_bearing + 180° - internal_angle
bearing2 = normalize_bearing(current_bearing + 180 - internal_angle2)
angle2_rad = bearing_to_radians(bearing2)
dx2 = length2 * math.cos(angle2_rad)
dy2 = length2 * math.sin(angle2_rad)
current_x += dx2
current_y += dy2
vertices.append((current_x, current_y))
print(f"Side 2: {length2:.1f}' @ {bearing2:.1f}° (internal angle {internal_angle2:.1f}°) -> Point ({current_x:.1f}, {current_y:.1f})")

current_bearing = bearing2

# Side 3: 21'2" with internal angle 113°03'
length3 = feet_inches_to_feet(21, 2)
internal_angle3 = 113 + 3/60  # 113°03' = 113.05°
bearing3 = normalize_bearing(current_bearing + 180 - internal_angle3)
angle3_rad = bearing_to_radians(bearing3)
dx3 = length3 * math.cos(angle3_rad)
dy3 = length3 * math.sin(angle3_rad)
current_x += dx3
current_y += dy3
vertices.append((current_x, current_y))
print(f"Side 3: {length3:.1f}' @ {bearing3:.1f}° (internal angle {internal_angle3:.1f}°) -> Point ({current_x:.1f}, {current_y:.1f})")

current_bearing = bearing3

# Side 4: 25' with external angle 135° (internal angle = 225°)
length4 = 25.0
external_angle4 = 135.0
internal_angle4 = 360 - external_angle4  # 225°
bearing4 = normalize_bearing(current_bearing + 180 - internal_angle4)
angle4_rad = bearing_to_radians(bearing4)
dx4 = length4 * math.cos(angle4_rad)
dy4 = length4 * math.sin(angle4_rad)
current_x += dx4
current_y += dy4
vertices.append((current_x, current_y))
print(f"Side 4: {length4}' @ {bearing4:.1f}° (external angle {external_angle4:.1f}°, internal angle {internal_angle4:.1f}°) -> Point ({current_x:.1f}, {current_y:.1f})")

current_bearing = bearing4

# Side 5: 92'2" with internal angle 57°09'
length5 = feet_inches_to_feet(92, 2)
internal_angle5 = 57 + 9/60  # 57°09' = 57.15°
bearing5 = normalize_bearing(current_bearing + 180 - internal_angle5)
angle5_rad = bearing_to_radians(bearing5)
dx5 = length5 * math.cos(angle5_rad)
dy5 = length5 * math.sin(angle5_rad)
current_x += dx5
current_y += dy5
vertices.append((current_x, current_y))
print(f"Side 5: {length5:.1f}' @ {bearing5:.1f}° (internal angle {internal_angle5:.1f}°) -> Point ({current_x:.1f}, {current_y:.1f})")

current_bearing = bearing5

# Side 6: 71' with internal angle (180-57°03') = 122°57'
length6 = 71.0
internal_angle6 = 180 - 57 - 3/60  # 122°57' = 122.95°
bearing6 = normalize_bearing(current_bearing + 180 - internal_angle6)
angle6_rad = bearing_to_radians(bearing6)
dx6 = length6 * math.cos(angle6_rad)
dy6 = length6 * math.sin(angle6_rad)
current_x += dx6
current_y += dy6
vertices.append((current_x, current_y))
print(f"Side 6: {length6:.1f}' @ {bearing6:.1f}° (internal angle {internal_angle6:.1f}°) -> Point ({current_x:.1f}, {current_y:.1f})")

print(f"\nFinal position after 6 sides: ({current_x:.1f}, {current_y:.1f})")
closure_error = math.sqrt(current_x**2 + current_y**2)
print(f"Closure error: {closure_error:.2f}' from origin")
print(f"Distance back to origin: {closure_error:.2f}'")

# Create bearings list for later use
bearings = [bearing1, bearing2, bearing3, bearing4, bearing5, bearing6]

# No rotation needed - we started with the correct bearing reference
print(f"No additional rotation needed - 60' side already at correct bearing {bearing1:.1f}° true")

# Calculate true bearings for display
true_bearings = [bearing1, bearing2, bearing3, bearing4, bearing5, bearing6]
side_names = ["60'", "87'1\"", "21'2\"", "25'", "92'2\"", "71'"]
print(f"\nTrue bearings:")
for i, (name, bearing) in enumerate(zip(side_names, true_bearings)):
    # Calculate magnetic bearing for reference  
    mag_bearing = normalize_bearing(bearing - magnetic_declination)
    print(f"Side {i+1} ({name}): {mag_bearing:.1f}° magnetic → {bearing:.1f}° true")

# Calculate area using shoelace formula
area = 0
n = len(vertices)
for i in range(n):
    j = (i + 1) % n
    area += vertices[i][0] * vertices[j][1]
    area -= vertices[j][0] * vertices[i][1]
area = abs(area) / 2

print(f"\nFinal area: {area:.1f} square feet ({area/43560:.4f} acres)")

# Create the plot
fig, ax = plt.subplots(1, 1, figsize=(12, 10))

# Plot the partial traverse (convert coordinates to meters for display)
x_coords = [v[0] * 0.3048 for v in vertices]
y_coords = [v[1] * 0.3048 for v in vertices]

# Draw the lines (using meter coordinates)
for i in range(len(x_coords)-1):
    ax.plot([x_coords[i], x_coords[i+1]], 
            [y_coords[i], y_coords[i+1]], 
            'b-', linewidth=3)

# Draw closure line (dashed red line back to origin)
closure_m = closure_error * 0.3048
ax.plot([x_coords[-1], x_coords[0]], 
        [y_coords[-1], y_coords[0]], 
        'r--', linewidth=2, alpha=0.7, label=f'Closure: {closure_m:.2f}m')
ax.legend()

# Plot vertices
ax.plot(x_coords, y_coords, 'ro', markersize=12)

# Add vertex labels (using meter coordinates)
for i, (x, y) in enumerate(zip(x_coords, y_coords)):
    ax.annotate(f'V{i+1}', (x, y), xytext=(10, 10), textcoords='offset points', 
                fontsize=16, fontweight='bold', color='darkred')

# Add side length and angle labels  
side_lengths = [60.0, feet_inches_to_feet(87, 1), feet_inches_to_feet(21, 2), 25.0, feet_inches_to_feet(92, 2), 71.0]
internal_angles = [None, internal_angle2, internal_angle3, internal_angle4, internal_angle5, internal_angle6]

for i in range(len(x_coords)-1):
    mid_x = (x_coords[i] + x_coords[i+1]) / 2
    mid_y = (y_coords[i] + y_coords[i+1]) / 2
    
    # Length label (convert to meters)
    length_m = side_lengths[i] * 0.3048
    if i == 2:  # 87'1"
        length_label = f"{length_m:.2f}m"
    elif i == 3:  # 21'2"
        length_label = f"{length_m:.2f}m"
    elif i == 5:  # 92'2"
        length_label = f"{length_m:.2f}m"
    else:
        length_label = f"{length_m:.2f}m"
    
    ax.annotate(length_label, (mid_x, mid_y), 
                xytext=(0, 20), textcoords='offset points',
                ha='center', fontsize=14, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.9))
    
    # Bearing label (show true bearing)
    true_bearing = true_bearings[i]
    ax.annotate(f'{true_bearing:.1f}° true', (mid_x, mid_y), 
                xytext=(0, -25), textcoords='offset points',
                ha='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.9))

# Add internal angle labels at vertices (using meter coordinates)
for i in range(1, len(x_coords)):
    if i < len(internal_angles) and internal_angles[i] is not None:
        x, y = x_coords[i], y_coords[i]
        ax.annotate(f'{internal_angles[i]:.1f}°', (x, y), 
                    xytext=(-30, -30), textcoords='offset points',
                    ha='center', fontsize=11, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.9))

# Add north arrow
ax.annotate('N', xy=(0.95, 0.95), xycoords='axes fraction', 
            fontsize=20, ha='center', va='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue'))
ax.annotate('↑', xy=(0.95, 0.91), xycoords='axes fraction', 
            fontsize=28, ha='center', va='center')

# Set equal aspect ratio (1:1 scale) and styling
ax.set_aspect('equal')
ax.grid(True, alpha=0.4, linestyle='-', linewidth=0.5)
ax.set_xlabel('East (meters)', fontsize=14)
ax.set_ylabel('North (meters)', fontsize=14)
# Convert area and closure to meters
area_m2 = area * 0.3048 * 0.3048
closure_m = closure_error * 0.3048
ax.set_title(f'Plot 7 - Complete Survey (True North)\n60\' @ 354°56\' true (340°6\' mag + 14°50\' decl.)\nArea: {area_m2:.0f} m² ({area_m2/10000:.4f} hectares) | Closure: {closure_m:.2f} m', fontsize=12, pad=20)

# Calculate perimeter for display
perimeter = sum(side_lengths)

# Add area text box on the plot (convert to meters)
area_m2 = area * 0.3048 * 0.3048
perimeter_m = perimeter * 0.3048
area_text = f"Area: {area_m2:.0f} m²\n({area_m2/10000:.4f} hectares)\nPerimeter: {perimeter_m:.2f} m"
ax.text(0.02, 0.98, area_text, transform=ax.transAxes, 
        fontsize=12, fontweight='bold', verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.9))

# Add margin around the plot (using meter coordinates)
x_min, x_max = min(x_coords), max(x_coords)
y_min, y_max = min(y_coords), max(y_coords)
x_range = x_max - x_min if x_max != x_min else 30  # 30 meters default
y_range = y_max - y_min if y_max != y_min else 30  # 30 meters default
margin = max(6, x_range * 0.2, y_range * 0.2)  # 6 meters minimum margin
ax.set_xlim(x_min - margin, x_max + margin)
ax.set_ylim(y_min - margin, y_max + margin)

plt.tight_layout()
plt.show()  # Show the plot

print(f"\nStep-by-step bearings:")
print(f"Side 1: {bearing1:.1f}° (60' @ 340°6' magnetic back-azimuth, 175° forward)")
print(f"Side 2: {bearing2:.1f}° (turn by {180-internal_angle2:.1f}°)")
print(f"Side 3: {bearing3:.1f}° (turn by {180-internal_angle3:.1f}°)")
print(f"Side 4: {bearing4:.1f}° (turn by {180-internal_angle4:.1f}°)")
print(f"Side 5: {bearing5:.1f}° (turn by {180-internal_angle5:.1f}°)")
print(f"Side 6: {bearing6:.1f}° (turn by {180-internal_angle6:.1f}°)")

# Calculate what bearing would be needed to close
close_bearing_rad = math.atan2(-current_y, -current_x)
close_bearing_deg = math.degrees(close_bearing_rad)
close_bearing_survey = 90 - close_bearing_deg
if close_bearing_survey < 0:
    close_bearing_survey += 360
print(f"\nTo close: need bearing {close_bearing_survey:.1f}° for {closure_error:.2f}'")

print(f"\nPolygon area: {area:.1f} square feet ({area/43560:.4f} acres)")

# Calculate perimeter
perimeter = sum(side_lengths)
print(f"Perimeter: {perimeter:.1f} feet")

# print(f"\n" + "="*50)
# print("GENERATING SVG FILE FOR INKSCAPE")
# print("="*50)

# SVG generation commented out
# Convert vertices to millimeters for SVG
# vertices_mm = []
# for x, y in vertices:
#     x_mm = x * 304.8
#     y_mm = y * 304.8
#     vertices_mm.append((x_mm, y_mm))

# print(f"SVG file created: plot7_survey.svg") 

print(f"\n" + "="*50)
print("FINAL VERTEX COORDINATES")
print("="*50)

# Output the final rotated vertices in millimeters (only the first 6 vertices - polygon)
vertices_mm = [(x * 304.8, y * 304.8) for x, y in vertices[:6]]  # Only first 6 vertices

print('\nVERTICES (millimeters):')
for i, (x, y) in enumerate(vertices_mm):
    print(f'V{i+1}: x={x:.1f}, y={y:.1f}')

print('\nVECTORS between vertices (millimeters):')
for i in range(len(vertices_mm)):
    j = (i + 1) % len(vertices_mm)
    dx = vertices_mm[j][0] - vertices_mm[i][0]
    dy = vertices_mm[j][1] - vertices_mm[i][1]
    length = math.sqrt(dx*dx + dy*dy)
    print(f'V{i+1} → V{j+1}: dx={dx:.1f}, dy={dy:.1f}, length={length:.1f}mm')

# Find bounding box
x_coords_mm = [v[0] for v in vertices_mm]
y_coords_mm = [v[1] for v in vertices_mm]

min_x, max_x = min(x_coords_mm), max(x_coords_mm)
min_y, max_y = min(y_coords_mm), max(y_coords_mm)

width_mm = max_x - min_x
height_mm = max_y - min_y

print(f'\nBOUNDING BOX:')
print(f'Width (x): {width_mm:.1f} millimeters')
print(f'Height (y): {height_mm:.1f} millimeters')
print(f'Min X: {min_x:.1f}, Max X: {max_x:.1f}')
print(f'Min Y: {min_y:.1f}, Max Y: {max_y:.1f}') 