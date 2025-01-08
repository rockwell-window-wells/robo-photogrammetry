import bpy
import os
from mathutils import Vector

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

# Input parameters
camera_positions_raw = [
    # (Camera position in WCS, Target position in WCS, Index)
    ([0.0, -12.0, 5.0], [-2.59, 9.68, 7], 0),
    ([0.0, -12.0, 10.0], [-2.59, 9.68, 7], 1),
    ([0.0, -12.0, 15.0], [-2.59, 9.68, 7], 2),
    ([0.0, -12.0, 5.0], [-7.4, 1.84, 2.7], 3),
    ([0.0, -12.0, 10.0], [-7.4, 1.84, 2.7], 4),
    ([0.0, -12.0, 15.0], [-7.4, 1.84, 2.7], 5),
    ([0.0, -12.0, 5.0], [6.68, 3.68, 9.0], 6),
    ([0.0, -12.0, 10.0], [6.68, 3.68, 9.0], 7),
    ([0.0, -12.0, 15.0], [6.68, 3.68, 9.0], 8),
]

# Pre-process to calculate direction vectors
camera_positions = [
    (camera_position, calculate_direction(camera_position, target_position), index)
    for camera_position, target_position, index in camera_positions_raw
]

output_directory = "C:/Users/Ryan.Larson.ROCKWELLINC/github"  # Change this to your desired directory

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Iterate through positions and render
for position, direction, index in camera_positions:
    camera = setup_camera(location=Vector(position), direction=direction)
    render_image(output_path=output_directory, index=index)

print("Rendering complete.")
