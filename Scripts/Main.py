# This is the file that executes all the code

import matplotlib.pyplot as plt
from tqdm import tqdm
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

LIDAR_RANGE = 50 # 50 meter
RESOLUTION = 10 # meter

risk_weights = (0.5, 1, 10)

map_name = 'boston-seaport'  #'singapore-onenorth'

map_width = 2979.5
map_height = 2118.1

x = 600 # ego_position[0][0]
y = 1600 # ego_position[0][1]
ego = (x, y)

filename = 'boston scene'

resolutions = [1]
scene_id = 1

def main(filename, id, LIDAR_RANGE, RESOLUTION):
    filename = f'{filename} {id} res = {RESOLUTION}'

    print("Starting main function...")  # Debugging line
    map = Map(dataroot, map_name, map_width, map_height, id, LIDAR_RANGE, RESOLUTION)

    # Create a folder to save the run and plots if it doesn't already exist
    run_folder = f"run {filename}"  # Include resolution in the plot folder name
    os.makedirs(run_folder, exist_ok=True)
    new_filename = os.path.join(run_folder, filename)

    # Assign layers to the grid in parallel
    map.assign_layer(new_filename, prnt=False)

    map.save_grid(new_filename + ' data')
    
    # Create a folder to save the run and plots if it doesn't already exist
    plots_folder = os.path.join(run_folder, 'plots')
    os.makedirs(plots_folder, exist_ok=True)

    # Layer plot filename
    layer_plot_filename = os.path.join(plots_folder, f"layer_plot_res={RESOLUTION}.png")
    Visualise.show_layers(map.grid)

    # Save the layer plot
    plt.savefig(layer_plot_filename)
    plt.close()
    print(f"Layer plot saved as '{layer_plot_filename}'.")

    # Initialize risk calculation
    risk = Risk()
    obj = Object(RESOLUTION,map, dataroot, map_name)
    dec = Detect(map, dataroot)

    # Calculate risk for each sample
    for i, sample in enumerate(map.samples):
        # do the object tracking risk and object detection risk by setting the sample
        # check if the tracking risk is already set, if not run the code to get the tracking risk 
        if (sum(cell.track_risk[i] for row in map.grid.grid for cell in row ) == 0):
            obj.sample = (sample,x,y,i)

        # check if the detection risk is already set, if not run the code to get the detection risk 
        # if (sum(cell.detect_risk[i] for row in map.grid.grid for cell in row ) == 0):
            # dec.sample = (sample,x,y)

        print(f"sample {i} complete")
        
        risk.CalcRisk(map, risk_weights, i)
        
        # Risk plot filename
        risk_plot_filename = os.path.join(plots_folder, f"risk_plot_iter_{i}_res={RESOLUTION}.png")
        Visualise.show_risks(map.grid, i)  # Show risks for the current iteration

        # Save the risk plot
        plt.savefig(risk_plot_filename)
        plt.close()  # Close the plot to free resources for the next iteration

        print(f"Risk plot for iteration {i} saved as '{risk_plot_filename}'.")
        
    
    # plot all risk plots with global maximum value 
    for i, sample in enumerate(map.samples):

        # Calculate the global maximum value across all total risk matrices
        max_total = max(np.max(np.array(matrix)) for matrix in [map.grid.get_total_risk_matrix(i) for i in range(map.grid.scene_length)])
        max_static = np.max(np.array(map.grid.get_static_risk_matrix()))
        max_detect = max(np.max(np.array(matrix)) for matrix in [map.grid.get_detect_risk_matrix(i) for i in range(map.grid.scene_length)])
        max_track = max(np.max(np.array(matrix)) for matrix in [map.grid.get_track_risk_matrix(i) for i in range(map.grid.scene_length)])

        risk_plot_filename = os.path.join(plots_folder, f"risk_plot_iter_{i}_res={RESOLUTION}.png")
        Visualise.show_risks(map.grid, i, max_total, max_static, max_detect, max_track)  # Show risks for the current iteration

        # Save the risk plot
        plt.savefig(risk_plot_filename)
        plt.close()  # Close the plot to free resources for the next iteration

        print(f"Risk plot for iteration {i} saved as '{risk_plot_filename}'.")

    # save the grid with the new risk values 
    map.save_grid(new_filename + ' data')
    print('Done')


# This ensures that the code is only executed when the script is run directly
if __name__ == '__main__':
    print("Running as main module...")  # Debugging line
    for res in resolutions:
        main(filename = 'boston scene', id=scene_id, LIDAR_RANGE=LIDAR_RANGE, RESOLUTION=res)
