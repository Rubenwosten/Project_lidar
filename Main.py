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

from nuscenes.nuscenes import NuScenes
from nuscenes.map_expansion.map_api import NuScenesMap
from nuscenes.map_expansion import arcline_path_utils
from nuscenes.map_expansion.bitmap import BitMap

LIDAR_RANGE = 5 # 50 meter
RESOLUTION = 1 # meter

dataroot = r'C:/Users/Ruben/OneDrive/Bureaublad/data/sets/nuscenes/' 
map_name = 'singapore-onenorth'

map_width = 2979.5
map_height = 2118.1

x = 360 # ego_position[0][0]
y = 1112 # ego_position[0][1]
ego = (x, y)

scene_id = 1

map = Map(dataroot, map_name, map_width, map_height, scene_id, LIDAR_RANGE, RESOLUTION)

map.assign_layer(prnt = False)

for sample in map.samples:
    Risk.CalcRisk()

Visualise.plot_grid(map.grid)

print('Done')
