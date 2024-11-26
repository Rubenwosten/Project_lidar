# This is the file that executes all the code

import matplotlib.pyplot as plt
import tqdm
import numpy as np
import re
import Cell
from Grid import Grid 
from Map import Map
from Visualise import Visualise

from nuscenes.nuscenes import NuScenes
from nuscenes.map_expansion.map_api import NuScenesMap
from nuscenes.map_expansion import arcline_path_utils
from nuscenes.map_expansion.bitmap import BitMap

dataroot = r'C:/Users/Chris/Python scripts/BEP VALDERS/data/sets/nuscenes'
map_name = 'singapore-onenorth'


map_width = 2979.5
map_height = 2118.1

map = Map(dataroot, map_name, map_width, map_height)

scene, first, last = map.get_scene(1)

LIDAR_RANGE = 10 # 50 meter
RESOLUTION = 0.5 # meter

samples,lidar_samples = map.samples_scene(first, last)
ego_position = map.ego_pos(lidar_samples)

x = 360 # ego_position[0][0]
y = 1112 # ego_position[0][1]

patch = ((x-10),(y-10),(x+10),(y+10))


x_min, x_max, y_min, y_max = map.minmax(x,y, LIDAR_RANGE)
grid = Grid(x_min, x_max, y_min, y_max, RESOLUTION)
map.assign_layer(grid, prnt = True)

Visualise.plot_grid(grid)

print('Done')
