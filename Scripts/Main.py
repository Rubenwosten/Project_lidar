# This is the file that executes all the code

import matplotlib.pyplot as plt
from tqdm import tqdm
import time
from datetime import timedelta
import numpy as np
import re
import Cell
import os
from Grid import Grid 
from Map import Map
from Visualise import Visualise
from Risk import Risk
from Object import Object
from Dectetion import Detect

from nuscenes.nuscenes import NuScenes
from nuscenes.map_expansion.map_api import NuScenesMap
from nuscenes.map_expansion import arcline_path_utils
from nuscenes.map_expansion.bitmap import BitMap

#dataroot = r"C:/Users/Ruben/OneDrive/Bureaublad/data/sets/nuscenes"
#dataroot = r"C:/Users/marni/OneDrive/Documents/BEP 2024/data/sets/nuscenes"
dataroot = r'C:/Users/Chris/Python scripts/BEP VALDERS/data/sets/nuscenes'

map_name = 'boston-seaport'  #'singapore-onenorth'
map_short = 'Boston'

map_width = 2979.5
map_height = 2118.1


LIDAR_RANGE = 100 # 100 meter
OCC_ACCUM = 1 / 8 # full accumulation in 8 samples = 4 sec 
LIDAR_DECAY = 0.1 # amount of occurrence that goes down per lidar point

risk_weights = (0.5, 2, 10)

scene_id = 1
RESOLUTION = 1 # meter

def main(map_short, id, LIDAR_RANGE, RESOLUTION, OCC_ACCUM, LIDAR_DECAY):

    print("Starting main function...")
    map = Map(dataroot, map_name, map_width, map_height, id, LIDAR_RANGE, RESOLUTION, OCC_ACCUM, LIDAR_DECAY)

    # Create a folder to save the run and plots if it doesn't already exist
    # Create the Run/Boston/scene 1 folder structure
    run_folder = os.path.join("Runs", map_short, f"scene {id} res={RESOLUTION}")
    os.makedirs(run_folder, exist_ok=True)

    plots_folder = os.path.join(run_folder,'plots')
    os.makedirs(plots_folder, exist_ok=True)

    gif_folder = os.path.join(run_folder,'GIFs')
    os.makedirs(gif_folder, exist_ok=True)

    # Paths for data, plots, and subfolders
    scene_data_path = os.path.join(run_folder, "data")
    layer_plot_path = os.path.join(plots_folder, "layers.png")
    risk_plots_folder = os.path.join(plots_folder, "risks")
    pointclouds_folder = os.path.join(plots_folder, "pointclouds")
    pointclouds_overlay_folder = os.path.join(plots_folder, "pointclouds overlay")
    
    # Create subfolders
    os.makedirs(risk_plots_folder, exist_ok=True)
    os.makedirs(pointclouds_folder, exist_ok=True)
    os.makedirs(pointclouds_overlay_folder, exist_ok=True)

    # Assign layers to the grid in parallel
    map.assign_layer(scene_data_path, prnt=False)

    map.save_grid(scene_data_path)

    # Generate and save the layer plot
    Visualise.show_layers(map.grid)
    plt.savefig(layer_plot_path)
    plt.close()
    print(f"Layer plot saved as '{layer_plot_path}'.\n")

    # Initialize risk calculation
    risk = Risk()
    obj = Object(RESOLUTION,map, dataroot, map_name)
    dec = Detect(map, dataroot, RESOLUTION)

    # Calculate risk for each sample
    for i, sample in enumerate(map.samples):
        # do the object tracking risk and object detection risk by setting the sample
        
        # check if the tracking risk is already set, if not run the code to get the tracking risk 
        #if (sum(cell.track_risk[i] for row in map.grid.grid for cell in row ) == 0):
            # obj.sample= (sample,0,0,i)
        #else:
        #    print('Tracking risk was already set, skipping the tracking risk calculations')

        obj.update(sample=sample,x=0,y=0,sample_index=i, prnt=False)

        #check if the detection risk is already set, if not run the code to get the detection risk 
        #if (sum(cell.detect_risk[i] for row in map.grid.grid for cell in row ) == 0):
        
        dec.update(sample=sample, sample_index=i, prnt=False)

        # Save individual pointcloud plots
        Visualise.save_pointcloud_scatterplot(map, dec.lidarpoint, i, pointclouds_folder, overlay=False)
        Visualise.save_pointcloud_scatterplot(map, dec.lidarpoint, i, pointclouds_overlay_folder, overlay=True)

        
        # Calculate risks
        risk.CalcRisk(map, risk_weights, i) 
        
        # Save individual risk plots
        risk_plot_filename = os.path.join(risk_plots_folder, f"risk_plot_iter_{i}.png")
        Visualise.show_risks(map.grid, i)
        plt.savefig(risk_plot_filename)
        plt.close() 
        print(f"Risk plot for iteration {i} saved as '{risk_plot_filename}'.")
        print(f"sample {i} complete\n")

        
    # Plot all risk plots with global maximum values
    max_total = max(np.max(np.array(matrix)) for matrix in [map.grid.get_total_risk_matrix(i) for i in range(map.grid.scene_length)])
    max_static = np.max(np.array(map.grid.get_static_risk_matrix()))
    max_detect = max(np.max(np.array(matrix)) for matrix in [map.grid.get_detect_risk_matrix(i) for i in range(map.grid.scene_length)])
    max_track = max(np.max(np.array(matrix)) for matrix in [map.grid.get_track_risk_matrix(i) for i in range(map.grid.scene_length)])
    
    for i, sample in enumerate(map.samples):
        risk_plot_filename = os.path.join(risk_plots_folder, f"risk_plot_iter_{i}.png")
        Visualise.show_risks_maximised(map.grid, i, max_total, max_static, max_detect, max_track)  
        plt.savefig(risk_plot_filename)
        plt.close()
        print(f"Risk plot for iteration {i} saved as '{risk_plot_filename}'.")

    # save the grid with the new risk values 
    map.save_grid(scene_data_path)

    # create gifs of all results
    Visualise.create_gif_from_folder(risk_plots_folder, os.path.join(gif_folder,'risks.gif'))
    Visualise.create_gif_from_folder(pointclouds_folder, os.path.join(gif_folder,'pointcloud.gif'))
    Visualise.create_gif_from_folder(pointclouds_overlay_folder, os.path.join(gif_folder,'pointcloud_layers.gif'))

    print('Done')


# This ensures that the code is only executed when the script is run directly
if __name__ == '__main__':
    print("Running as main module...")  # Debugging line
    start_time = time.time()
    main(map_short=map_short, id=scene_id, LIDAR_RANGE=LIDAR_RANGE, RESOLUTION=RESOLUTION, OCC_ACCUM=OCC_ACCUM, LIDAR_DECAY=LIDAR_DECAY)

    run_time = time.time() - start_time
    print(f'\nRunning took {timedelta(seconds=run_time)}')