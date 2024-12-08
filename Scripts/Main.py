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

LIDAR_RANGE = 50 # 50 meter
RESOLUTION = 2 # meter

risk_weights = (1, 1, 1) 
#dataroot = r"C:/Users/Ruben/OneDrive/Bureaublad/data/sets/nuscenes"
#dataroot = r"C:/Users/marni/OneDrive/Documents/BEP 2024/data/sets/nuscenes"
dataroot = r'C:/Users/Chris/Python scripts/BEP VALDERS/data/sets/nuscenes'

map_name = 'boston-seaport'  #'singapore-onenorth'

map_width = 2979.5
map_height = 2118.1

scene_id = 1

filename = f'boston scene {scene_id} res = {RESOLUTION}'

def main():
    print("Starting main function...")  # Debugging line
    map = Map(dataroot, map_name, map_width, map_height, scene_id, LIDAR_RANGE, RESOLUTION)

    # Create a folder to save the run and plots if it doesn't already exist
    run_folder = f"run {filename}"  # Include resolution in the plot folder name
    os.makedirs(run_folder, exist_ok=True)
    new_filename = os.path.join(run_folder, filename)

    # Assign layers to the grid in parallel
    map.assign_layer(new_filename, prnt=False)


    map.assign_layer(filename, prnt=False)

    # Initialize risk calculation
    risk = Risk()
    #obj = Object(RESOLUTION, map, dataroot)
    #dec = Detect(map, dataroot)

    # Calculate risk for each sample        
    for i, sample in enumerate(map.samples):
        #dec.sample = sample
        risk.CalcRisk(map, risk_weights, i)

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

    # Calculate risk for each sample and save the plot
    for i, sample in enumerate(map.samples):
    # Initialize risk calculation
    risk = Risk()
    obj = Object(RESOLUTION,map, dataroot, map_name)
    dec = Detect(map, dataroot, x, y)

    # Calculate risk for each sample
    for i in range(len(map.samples)):
        sample = map.samples[i]
        obj.sample= (sample,x,y,i)
        print ("sample complete")
        #dec.sample = (sample,x,y)
        
        risk.CalcRisk(map, risk_weights, i)
        

        # Risk plot filename
        risk_plot_filename = os.path.join(plots_folder, f"risk_plot_iter_{i}_res={RESOLUTION}.png")
        Visualise.show_risks(map.grid, i)  # Show risks for the current iteration

        # Save the risk plot
        plt.savefig(risk_plot_filename)
        plt.close()  # Close the plot to free resources for the next iteration

        print(f"Risk plot for iteration {i} saved as '{risk_plot_filename}'.")

    print('Done')

# This ensures that the code is only executed when the script is run directly
if __name__ == '__main__':
    print("Running as main module...")  # Debugging line
    main()