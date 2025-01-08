# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 12:55:04 2025

@author: Ryan.Larson
"""

import pycolmap
import csv
import numpy as np
import os
import subprocess
import json

def create_camera_intrinsic(f_mm, sensor_width, image_width, image_height):
    """
    Convert Blender camera parameters to Meshroom-compatible intrinsics.
    
    Args:
        f_mm (float): Focal length in millimeters.
        sensor_width (float): Sensor width in millimeters.
        image_width (int): Image width in pixels.
        image_height (int): Image height in pixels.
    
    Returns:
        dict: Meshroom camera parameters.
    """
    # Calculate focal lengths in pixels
    fx = (f_mm / sensor_width) * image_width
    fy = (f_mm / sensor_width) * image_height  # Assuming square sensor
    
    # Principal point at the center
    cx = image_width / 2
    cy = image_height / 2

    # Return COLMAP camera parameters
    camera_params = {
        "cameraModel": "pinhole",
        "intrinsic": {
          "fx": fx,
          "fy": fy,
          "cx": cx,
          "cy": cy,
          "width": image_width,
          "height": image_height
        }
    }
    return camera_params

if __name__ == "__main__":
    # Set paths
    meshroom_path = r"C:\path\to\Meshroom"  # Update this to the correct Meshroom path
    images_folder = r"C:\Users\Ryan.Larson.ROCKWELLINC\github\robo-photogrammetry\images"  # Folder with your rendered images
    output_folder = r"C:\Users\Ryan.Larson.ROCKWELLINC\github\robo-photogrammetry\output"  # Folder where the output model will be saved
    camera_params_path = r"C:\Users\Ryan.Larson.ROCKWELLINC\github\robo-photogrammetry\camera_params.json"
    
    # Camera values from Blender
    f_mm = 35.0  # Focal length in mm
    sensor_width = 36.0  # Sensor width in mm
    image_width = 1920  # Image resolution width in pixels
    image_height = 1080  # Image resolution height in pixels
    
    camera_params = create_camera_intrinsic(f_mm, sensor_width, image_width, image_height)
    with open(camera_params_path, "w") as file:
        json.dump(camera_params, file)
    
    # Step 1: Create a project folder and set up the Meshroom project
    project_name = "MeshroomProject"
    project_path = os.path.join(output_folder, project_name)
    
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    
    # Step 2: Define the Meshroom command to run the reconstruction
    meshroom_command = [
        os.path.join(meshroom_path, "meshroom_photogrammetry"),
        "--imageFolder", images_folder,
        "--output", project_path,
        "--cameraModels", "Pinhole",
        "--cameraIntrinsic", camera_params_path
    ]
    
    # Optionally, specify camera parameters if you have a calibration file:
    # --cameraModels and --cameraIntrinsic
    # meshroom_command.extend([
    #     "--cameraModels", "Pinhole",
    #     "--cameraIntrinsic", "camera_intrinsic.json"
    # ])
    
    # Step 3: Run the reconstruction
    try:
        print("Starting Meshroom photogrammetry process...")
        subprocess.run(meshroom_command, check=True)
        print(f"Reconstruction complete. The model is saved in {project_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during Meshroom reconstruction: {e}")


# # Define paths
# image_folder = "C:/Users/Ryan.Larson.ROCKWELLINC/github/robo-photogrammetry/images"  # Folder containing your images
# output_folder = "C:/Users/Ryan.Larson.ROCKWELLINC/github/robo-photogrammetry/output"  # Folder where the COLMAP database and output will be saved

# # Step 1: Initialize COLMAP project
# def initialize_project(image_folder, output_folder):
#     """
#     Initializes the COLMAP project by creating necessary directories and database.
#     """
#     import os
#     from pathlib import Path

#     # Ensure the output folder exists
#     Path(output_folder).mkdir(parents=True, exist_ok=True)

#     # Initialize the database
#     db_path = os.path.join(output_folder, "database.db")
#     pycolmap.database.create_empty_database(db_path)

#     print(f"COLMAP project initialized. Database created at {db_path}")
#     return db_path

# def blender_to_colmap(f_mm, sensor_width, image_width, image_height):
#     """
#     Convert Blender camera parameters to COLMAP-compatible intrinsics.
    
#     Args:
#         f_mm (float): Focal length in millimeters.
#         sensor_width (float): Sensor width in millimeters.
#         image_width (int): Image width in pixels.
#         image_height (int): Image height in pixels.
    
#     Returns:
#         dict: COLMAP camera parameters.
#     """
#     # Calculate focal lengths in pixels
#     fx = (f_mm / sensor_width) * image_width
#     fy = (f_mm / sensor_width) * image_height  # Assuming square sensor
    
#     # Principal point at the center
#     cx = image_width / 2
#     cy = image_height / 2

#     # Return COLMAP camera parameters
#     camera_params = {
#         "camera_id": 1,
#         "model": "PINHOLE",
#         "width": image_width,
#         "height": image_height,
#         "params": [fx, fy, cx, cy],
#     }
#     return camera_params

# def compute_camera_extrinsics(position, direction):
#     # Normalize the direction vector
#     direction = np.array(direction)
#     direction = direction / np.linalg.norm(direction)

#     # Camera coordinate system:
#     # z-axis: -direction (camera looks along the negative z-axis)
#     z_axis = -direction

#     # Create an arbitrary up vector (not parallel to the direction)
#     up = np.array([0.0, 1.0, 0.0])
#     if np.abs(np.dot(z_axis, up)) > 0.99:  # If too close to parallel, use a different up vector
#         up = np.array([1.0, 0.0, 0.0])

#     # x-axis: cross product of up and z-axis
#     x_axis = np.cross(up, z_axis)
#     x_axis = x_axis / np.linalg.norm(x_axis)

#     # y-axis: cross product of z and x to ensure orthogonality
#     y_axis = np.cross(z_axis, x_axis)
#     y_axis = y_axis / np.linalg.norm(y_axis)

#     # Rotation matrix: [x_axis, y_axis, z_axis] (column vectors)
#     rotation_matrix = np.stack([x_axis, y_axis, z_axis], axis=1)

#     # Translation vector (negative because COLMAP expects world to camera transformation)
#     translation_vector = -np.dot(rotation_matrix, np.array(position))

#     return rotation_matrix, translation_vector

# def save_extrinsics_to_file(csv_file, output_file):
#     with open(csv_file, 'r') as f:
#         reader = csv.DictReader(f, delimiter='\t')
#         with open(output_file, 'w') as out_f:
#             out_f.write('# Camera extrinsics for COLMAP\n')
#             out_f.write('# Format: <camera_id> <rotation_matrix (9 values)> <translation_vector (3 values)>\n')
#             for row in reader:
#                 position = eval(row['camera_position'])  # Convert string to list
#                 direction = eval(row['direction'])  # Convert string to list
#                 camera_id = row['index']
                
#                 # Compute extrinsics
#                 rotation_matrix, translation_vector = compute_camera_extrinsics(position, direction)
                
#                 # Flatten rotation matrix
#                 rotation_flat = rotation_matrix.flatten()
                
#                 # Write to output file
#                 out_f.write(f'{camera_id} {" ".join(map(str, rotation_flat))} {" ".join(map(str, translation_vector))}\n')

# # Step 2: Run the reconstruction pipeline
# def run_reconstruction(image_folder, output_folder, db_path):
#     """
#     Runs the COLMAP reconstruction pipeline: feature extraction, matching, and reconstruction.
#     """
#     # Feature extraction
#     print("Extracting features...")
#     pycolmap.extract_features(db_path, image_folder)

#     # Feature matching
#     print("Matching features...")
#     pycolmap.match_exhaustive(db_path)

#     # Reconstruction
#     print("Starting sparse reconstruction...")
#     reconstruction_path = pycolmap.sparse_reconstruction(image_folder, db_path, output_folder)
#     print(f"Sparse reconstruction completed. Results saved at {reconstruction_path}")

#     # (Optional) Dense reconstruction
#     print("Starting dense reconstruction...")
#     dense_reconstruction_path = pycolmap.dense_reconstruction(reconstruction_path)
#     print(f"Dense reconstruction completed. Results saved at {dense_reconstruction_path}")

#     return reconstruction_path, dense_reconstruction_path

# # Main script
# if __name__ == "__main__":
#     # Initialize the project
#     database_path = initialize_project(image_folder, output_folder)
    
#     # Example values from Blender
#     f_mm = 35.0  # Focal length in mm
#     sensor_width = 36.0  # Sensor width in mm
#     image_width = 1920  # Image resolution width in pixels
#     image_height = 1080  # Image resolution height in pixels
    
#     camera_params = blender_to_colmap(f_mm, sensor_width, image_width, image_height)
    
#     # Register the camera
#     camera_id = pycolmap.database.add_camera(
#         database_path,
#         model=camera_params["model"],
#         width=camera_params["width"],
#         height=camera_params["height"],
#         params=camera_params["params"],
#     )
#     print(f"Camera registered with ID: {camera_id}")
    
#     csv_file = 'C:/Users/Ryan.Larson.ROCKWELLINC/github/robo-photogrammetry/camera_positions.csv'  # Replace with your CSV file path
#     output_file = 'C:/Users/Ryan.Larson.ROCKWELLINC/github/robo-photogrammetry/camera_extrinsics.txt'
    
#     # Generate COLMAP camera extrinsics
#     save_extrinsics_to_file(csv_file, output_file)
#     print(f"Camera extrinsics saved to {output_file}")

#     # # Run the reconstruction pipeline
#     # sparse_model_path, dense_model_path = run_reconstruction(image_folder, output_folder, database_path)

#     # print("Photogrammetry process completed.")
#     # print(f"Sparse model saved at: {sparse_model_path}")
#     # print(f"Dense model saved at: {dense_model_path}")
