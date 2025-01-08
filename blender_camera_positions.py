import bpy
import os
from mathutils import Vector
import csv

def calculate_direction(camera_position, target_position):
    """Calculate the direction vector from camera position to target position."""
    return Vector(camera_position) - Vector(target_position)

def setup_camera(location, direction):
    """Set up the camera at a specific location and direction."""
    # Ensure a camera exists
    if "Camera" not in bpy.data.objects:
        bpy.ops.object.camera_add()
    camera = bpy.data.objects["Camera"]

    # Set camera location
    camera.location = location

    # Set camera direction
    direction.normalize()
    camera.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()

    return camera

def render_image(output_path, index):
    """Render the scene and save the image."""
    bpy.context.scene.render.filepath = os.path.join(output_path, f"render_{index}.png")
    bpy.ops.render.render(write_still=True)

def generate_camera_positions_raw(camera_coords, target_coords):
    camera_positions_raw = []
    index = 0
    for i, camera_coord in enumerate(camera_coords):
        for j, target_coord in enumerate(target_coords):
            camera_positions_raw.append((camera_coord, target_coord, index))
            index += 1
    return camera_positions_raw

camera_z = [0.25, 0.5, 0.75, 1.125]
camera_coords = [[0.0, -0.92, z] for z in camera_z]

target_z = [0.125, 0.375, 0.625, 0.875, 1.0]
target_xy = [
    [-0.65, 0.39],
    [-0.5, 0.78],
    [-0.375, 0.91],
    [-0.25, 1.0],
    [0.0, 1.0],
    [0.25, 1.0],
    [0.375, 0.91],
    [0.5, 0.78],
    [0.65, 0.39],
    ]

target_coords = []
for z in target_z:
    for xy in target_xy:
        target_coords.append([xy[0], xy[1], z])

camera_positions_raw = generate_camera_positions_raw(camera_coords, target_coords)

# # Input parameters
# camera_positions_raw = [
#     # (Camera position in WCS, Target position in WCS, Index)
#     ([0.0, -12.0, 5.0], [-2.59, 9.68, 7], 0),
#     ([0.0, -12.0, 10.0], [-2.59, 9.68, 7], 1),
#     ([0.0, -12.0, 15.0], [-2.59, 9.68, 7], 2),
#     ([0.0, -12.0, 5.0], [-7.4, 1.84, 2.7], 3),
#     ([0.0, -12.0, 10.0], [-7.4, 1.84, 2.7], 4),
#     ([0.0, -12.0, 15.0], [-7.4, 1.84, 2.7], 5),
#     ([0.0, -12.0, 5.0], [6.68, 3.68, 9.0], 6),
#     ([0.0, -12.0, 10.0], [6.68, 3.68, 9.0], 7),
#     ([0.0, -12.0, 15.0], [6.68, 3.68, 9.0], 8),
# ]

# Pre-process to calculate direction vectors
camera_positions = [
    (camera_position, calculate_direction(camera_position, target_position), index)
    for camera_position, target_position, index in camera_positions_raw
]

# Save the camera positions and direction vectors
data = [["camera_position", "direction", "index"]]
for row in camera_positions:
    data.append([row[0], list(row[1].normalized()), row[2]])

csv_filepath = "C:/Users/Ryan.Larson.ROCKWELLINC/github/robo-photogrammetry/camera_positions.csv"
with open(csv_filepath, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

output_directory = "C:/Users/Ryan.Larson.ROCKWELLINC/github/robo-photogrammetry/images"  # Change this to your desired directory

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Iterate through positions and render
for position, direction, index in camera_positions:
    camera = setup_camera(location=Vector(position), direction=direction)
    render_image(output_path=output_directory, index=index)

print("Rendering complete.")
