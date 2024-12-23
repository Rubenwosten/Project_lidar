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


#dataroot = r'C:/Users/marni/OneDrive/Documents/BEP 2024/data/sets/nuscenes'
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
RESOLUTION = 10 # meter

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

# Generate and save the layer plot
Visualise.show_layers(map.grid)
plt.savefig(layer_plot_path)
plt.close()
print(f"Layer plot saved as '{layer_plot_path}'.\n")

# create gifs of all results
Visualise.create_gif_from_folder(risk_plots_folder, os.path.join(gif_folder,'risks.gif'))
Visualise.create_gif_from_folder(pointclouds_folder, os.path.join(gif_folder,'pointcloud.gif'))
Visualise.create_gif_from_folder(pointclouds_overlay_folder, os.path.join(gif_folder,'pointcloud_layers.gif'))

print('Done')



