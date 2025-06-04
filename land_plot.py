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

# Side 1: 71' horizontal (due east for simplicity)
length1 = 71.0
bearing1 = 90.0  # Due east - perfectly horizontal
angle1_rad = bearing_to_radians(bearing1)
dx1 = length1 * math.cos(angle1_rad)
dy1 = length1 * math.sin(angle1_rad)
current_x += dx1
current_y += dy1
vertices.append((current_x, current_y))
print(f"Side 1: {length1}' @ {bearing1:.1f}° (horizontal) -> Point ({current_x:.1f}, {current_y:.1f})")

current_bearing = bearing1

# Side 2: 60' with internal angle 89°41'
length2 = 60.0
internal_angle2 = 89 + 41/60  # 89°41' = 89.683°
# Calculate next bearing: current_bearing + 180° - internal_angle
bearing2 = normalize_bearing(current_bearing + 180 - internal_angle2)
angle2_rad = bearing_to_radians(bearing2)
dx2 = length2 * math.cos(angle2_rad)
dy2 = length2 * math.sin(angle2_rad)
current_x += dx2
current_y += dy2
vertices.append((current_x, current_y))
print(f"Side 2: {length2}' @ {bearing2:.1f}° (internal angle {internal_angle2:.1f}°) -> Point ({current_x:.1f}, {current_y:.1f})")

current_bearing = bearing2

# Side 3: 87'1" with internal angle (180° - 67°50') = 112°10'
length3 = feet_inches_to_feet(87, 1)
internal_angle3 = 180 - 67 - 50/60  # 112°10' = 112.167°
bearing3 = normalize_bearing(current_bearing + 180 - internal_angle3)
angle3_rad = bearing_to_radians(bearing3)
dx3 = length3 * math.cos(angle3_rad)
dy3 = length3 * math.sin(angle3_rad)
current_x += dx3
current_y += dy3
vertices.append((current_x, current_y))
print(f"Side 3: {length3:.1f}' @ {bearing3:.1f}° (internal angle {internal_angle3:.1f}°) -> Point ({current_x:.1f}, {current_y:.1f})")

current_bearing = bearing3

# Side 4: 21'2" with internal angle 113°03'
length4 = feet_inches_to_feet(21, 2)
internal_angle4 = 113 + 3/60  # 113°03' = 113.05°
bearing4 = normalize_bearing(current_bearing + 180 - internal_angle4)
angle4_rad = bearing_to_radians(bearing4)
dx4 = length4 * math.cos(angle4_rad)
dy4 = length4 * math.sin(angle4_rad)
current_x += dx4
current_y += dy4
vertices.append((current_x, current_y))
print(f"Side 4: {length4:.1f}' @ {bearing4:.1f}° (internal angle {internal_angle4:.1f}°) -> Point ({current_x:.1f}, {current_y:.1f})")

current_bearing = bearing4

# Side 5: 25' with external angle 135° (internal angle = 225°)
length5 = 25.0
external_angle5 = 135.0
internal_angle5 = 360 - external_angle5  # 225°
bearing5 = normalize_bearing(current_bearing + 180 - internal_angle5)
angle5_rad = bearing_to_radians(bearing5)
dx5 = length5 * math.cos(angle5_rad)
dy5 = length5 * math.sin(angle5_rad)
current_x += dx5
current_y += dy5
vertices.append((current_x, current_y))
print(f"Side 5: {length5}' @ {bearing5:.1f}° (external angle {external_angle5:.1f}°, internal angle {internal_angle5:.1f}°) -> Point ({current_x:.1f}, {current_y:.1f})")

current_bearing = bearing5

# Side 6: 92'2" with internal angle 57°09'
length6 = feet_inches_to_feet(92, 2)
internal_angle6 = 57 + 9/60  # 57°09' = 57.15°
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

# Now rotate the polygon so the 60' side has the correct bearing of 340°6' magnetic
# Currently the 60' side (side 2) has bearing 180.3°, but it should be 340°6'
target_magnetic_bearing = 340 + 6/60  # 340.1°
current_60_bearing = bearing2  # 180.3°
rotation_needed = target_magnetic_bearing - current_60_bearing
if rotation_needed < -180:
    rotation_needed += 360
elif rotation_needed > 180:
    rotation_needed -= 360

print(f"\nRotation correction needed: {rotation_needed:.1f}°")

# Apply rotation to all vertices
rotation_rad = math.radians(rotation_needed)
cos_rot = math.cos(rotation_rad)
sin_rot = math.sin(rotation_rad)

rotated_vertices = []
for x, y in vertices:
    new_x = x * cos_rot - y * sin_rot
    new_y = x * sin_rot + y * cos_rot
    rotated_vertices.append((new_x, new_y))

# Apply magnetic declination correction for Adelaide 1961: +10°50'
magnetic_declination = 10 + 50/60  # 10°50'
print(f"Applying magnetic declination for Adelaide 1961: +{magnetic_declination:.1f}°")

# Recalculate all bearings with corrections
corrected_bearings = []
for bearing in bearings:
    # First apply rotation
    corrected_bearing = normalize_bearing(bearing + rotation_needed)
    # Then apply magnetic declination to get true bearing
    true_bearing = normalize_bearing(corrected_bearing + magnetic_declination)
    corrected_bearings.append(true_bearing)

print(f"\nCorrected bearings (True North):")
side_names = ["71'", "60'", "87'1\"", "21'2\"", "25'", "92'2\""]
for i, (name, mag_bear, true_bear) in enumerate(zip(side_names, bearings, corrected_bearings)):
    mag_corrected = normalize_bearing(bearings[i] + rotation_needed)
    print(f"Side {i+1} ({name}): {mag_corrected:.1f}° magnetic → {true_bear:.1f}° true")

# Update vertices for plotting
vertices = rotated_vertices

# Create the plot
fig, ax = plt.subplots(1, 1, figsize=(12, 10))

# Plot the partial traverse
x_coords = [v[0] for v in vertices]
y_coords = [v[1] for v in vertices]

# Draw the lines
for i in range(len(vertices)-1):
    ax.plot([vertices[i][0], vertices[i+1][0]], 
            [vertices[i][1], vertices[i+1][1]], 
            'b-', linewidth=3)

# Draw closure line (dashed red line back to origin)
ax.plot([vertices[-1][0], vertices[0][0]], 
        [vertices[-1][1], vertices[0][1]], 
        'r--', linewidth=2, alpha=0.7, label=f'Closure: {closure_error:.1f}\'')
ax.legend()

# Plot vertices
ax.plot(x_coords, y_coords, 'ro', markersize=12)

# Add vertex labels
for i, (x, y) in enumerate(vertices):
    ax.annotate(f'V{i+1}', (x, y), xytext=(10, 10), textcoords='offset points', 
                fontsize=16, fontweight='bold', color='darkred')

# Add side length and angle labels
side_lengths = [71.0, 60.0, feet_inches_to_feet(87, 1), feet_inches_to_feet(21, 2), 25.0, feet_inches_to_feet(92, 2)]
internal_angles = [None, internal_angle2, internal_angle3, internal_angle4, internal_angle5, internal_angle6]

for i in range(len(vertices)-1):
    mid_x = (vertices[i][0] + vertices[i+1][0]) / 2
    mid_y = (vertices[i][1] + vertices[i+1][1]) / 2
    
    # Length label
    if i == 2:  # 87'1"
        length_label = "87'1\""
    elif i == 3:  # 21'2"
        length_label = "21'2\""
    elif i == 5:  # 92'2"
        length_label = "92'2\""
    else:
        length_label = f"{side_lengths[i]:.0f}'"
    
    ax.annotate(length_label, (mid_x, mid_y), 
                xytext=(0, 20), textcoords='offset points',
                ha='center', fontsize=14, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.9))
    
    # Bearing label (show corrected magnetic bearing)
    corrected_mag_bearing = normalize_bearing(bearings[i] + rotation_needed)
    ax.annotate(f'{corrected_mag_bearing:.1f}° mag', (mid_x, mid_y), 
                xytext=(0, -25), textcoords='offset points',
                ha='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.9))

# Add internal angle labels at vertices
for i in range(1, len(vertices)):
    if i < len(internal_angles) and internal_angles[i] is not None:
        x, y = vertices[i]
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

# Set equal aspect ratio and styling
ax.set_aspect('equal')
ax.grid(True, alpha=0.4, linestyle='-', linewidth=0.5)
ax.set_xlabel('East (feet)', fontsize=14)
ax.set_ylabel('North (feet)', fontsize=14)
ax.set_title(f'Plot 7 - Complete Survey (Corrected)\n60\' @ 340°6\' magnetic, Adelaide 1961 (+10°50\' decl.)\nClosure Error: {closure_error:.2f} feet', fontsize=14, pad=20)

# Add margin around the plot
x_min, x_max = min(x_coords), max(x_coords)
y_min, y_max = min(y_coords), max(y_coords)
x_range = x_max - x_min if x_max != x_min else 100
y_range = y_max - y_min if y_max != y_min else 100
margin = max(20, x_range * 0.2, y_range * 0.2)
ax.set_xlim(x_min - margin, x_max + margin)
ax.set_ylim(y_min - margin, y_max + margin)

plt.tight_layout()
plt.show()

print(f"\nStep-by-step bearings:")
print(f"Side 1: {bearing1:.1f}° (horizontal baseline)")
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