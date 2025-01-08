# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 12:55:04 2025

@author: Ryan.Larson
"""

import pycolmap

# Define paths
image_folder = "C:/Users/Ryan.Larson.ROCKWELLINC/github/robo-photogrammetry/images"  # Folder containing your images
output_folder = "C:/Users/Ryan.Larson.ROCKWELLINC/github/robo-photogrammetry/output"  # Folder where the COLMAP database and output will be saved

# Step 1: Initialize COLMAP project
def initialize_project(image_folder, output_folder):
    """
    Initializes the COLMAP project by creating necessary directories and database.
    """
    import os
    from pathlib import Path

    # Ensure the output folder exists
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Initialize the database
    db_path = os.path.join(output_folder, "database.db")
    pycolmap.database.create_empty_database(db_path)

    print(f"COLMAP project initialized. Database created at {db_path}")
    return db_path

def blender_to_colmap(f_mm, sensor_width, image_width, image_height):
    """
    Convert Blender camera parameters to COLMAP-compatible intrinsics.
    
    Args:
        f_mm (float): Focal length in millimeters.
        sensor_width (float): Sensor width in millimeters.
        image_width (int): Image width in pixels.
        image_height (int): Image height in pixels.
    
    Returns:
        dict: COLMAP camera parameters.
    """
    # Calculate focal lengths in pixels
    fx = (f_mm / sensor_width) * image_width
    fy = (f_mm / sensor_width) * image_height  # Assuming square sensor
    
    # Principal point at the center
    cx = image_width / 2
    cy = image_height / 2

    # Return COLMAP camera parameters
    camera_params = {
        "camera_id": 1,
        "model": "PINHOLE",
        "width": image_width,
        "height": image_height,
        "params": [fx, fy, cx, cy],
    }
    return camera_params

# Step 2: Run the reconstruction pipeline
def run_reconstruction(image_folder, output_folder, db_path):
    """
    Runs the COLMAP reconstruction pipeline: feature extraction, matching, and reconstruction.
    """
    # Feature extraction
    print("Extracting features...")
    pycolmap.extract_features(image_folder, db_path)

    # Feature matching
    print("Matching features...")
    pycolmap.match_features(db_path)

    # Reconstruction
    print("Starting sparse reconstruction...")
    reconstruction_path = pycolmap.sparse_reconstruction(image_folder, db_path, output_folder)
    print(f"Sparse reconstruction completed. Results saved at {reconstruction_path}")

    # (Optional) Dense reconstruction
    print("Starting dense reconstruction...")
    dense_reconstruction_path = pycolmap.dense_reconstruction(reconstruction_path)
    print(f"Dense reconstruction completed. Results saved at {dense_reconstruction_path}")

    return reconstruction_path, dense_reconstruction_path

# Main script
if __name__ == "__main__":
    # Initialize the project
    database_path = initialize_project(image_folder, output_folder)
    
    # Example values from Blender
    f_mm = 35.0  # Focal length in mm
    sensor_width = 36.0  # Sensor width in mm
    image_width = 1920  # Image resolution width in pixels
    image_height = 1080  # Image resolution height in pixels
    
    camera_params = blender_to_colmap(f_mm, sensor_width, image_width, image_height)
    
    # Register the camera
    camera_id = pycolmap.database.add_camera(
        database_path,
        model=camera_params["model"],
        width=camera_params["width"],
        height=camera_params["height"],
        params=camera_params["params"],
    )
    print(f"Camera registered with ID: {camera_id}")

    # Run the reconstruction pipeline
    sparse_model_path, dense_model_path = run_reconstruction(image_folder, output_folder, database_path)

    print("Photogrammetry process completed.")
    print(f"Sparse model saved at: {sparse_model_path}")
    print(f"Dense model saved at: {dense_model_path}")
