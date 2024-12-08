# This is the file that executes all the code

import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import re
import Cell
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
dataroot = r"C:/Users/Ruben/OneDrive/Bureaublad/data/sets/nuscenes"
#dataroot = r"C:/Users/marni/OneDrive/Documents/BEP 2024/data/sets/nuscenes"
#dataroot = r'C:/Users/Chris/Python scripts/BEP VALDERS/data/sets/nuscenes'

map_name = 'boston-seaport'  #'singapore-onenorth'

map_width = 2979.5
map_height = 2118.1

<<<<<<< HEAD
x = 600 # ego_position[0][0]
y = 1600 # ego_position[0][1]
ego = (x, y)

=======
>>>>>>> c8b0d3b355fa9ba76105a557e0a3ad612157d055
scene_id = 1

filename = 'boston scene 1'

def main():
    print("Starting main function...")  # Debugging line
    map = Map(dataroot, map_name, map_width, map_height, scene_id, LIDAR_RANGE, RESOLUTION)

    # Assign layers to the grid in parallel
    map.assign_layer(filename, prnt=False)

    # Initialize risk calculation
    risk = Risk()
    obj = Object(RESOLUTION,map)
    dec = Detect(map, dataroot,x,y)

<<<<<<< HEAD
    # Calculate risk for each sample
    sample = map.samples[4]
    obj.sample= (sample,x,y)
    print ("sample complete")
        #dec.sample = (sample,x,y)
        
    risk.CalcRisk(map, risk_weights)
        
        
=======
    # Calculate risk for each sample        
    for i, sample in enumerate(map.samples):
        dec.sample = sample
        risk.CalcRisk(map, risk_weights, i)
        print ("sample complete ja ja ja ja ja ja ja ja ja ja ja ja ja ja ja ja ja ja")
>>>>>>> c8b0d3b355fa9ba76105a557e0a3ad612157d055

    map.save_grid(filename)
    
    # Visualize the grid
    Visualise.plot_grid(map.grid, 0)

    print('Done')

# This ensures that the code is only executed when the script is run directly
if __name__ == '__main__':
    print("Running as main module...")  # Debugging line
    main()