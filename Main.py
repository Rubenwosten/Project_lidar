# This is the file that executes all the code

import matplotlib.pyplot as plt
import tqdm
import numpy as np
import re
import Cell
import Grid
import Map
import Visualise

from nuscenes.nuscenes import NuScenes
from nuscenes.map_expansion.map_api import NuScenesMap
from nuscenes.map_expansion import arcline_path_utils
from nuscenes.map_expansion.bitmap import BitMap
 
nusc = NuScenes(version='v1.0-mini', verbose=False)

nusc_map = NuScenesMap(dataroot='C:/Users/Ruben/OneDrive/Bureaublad/data/sets/nuscenes/v1.0-mini', map_name='singapore-onenorth')
bitmap = BitMap(nusc_map.dataroot, nusc_map.map_name, 'basemap')


map_width = 2979.5
map_height = 2118.1
#sample array
scene = nusc.scene[1]
first = scene['first_sample_token']
last = scene['last_sample_token']


LIDAR_RANGE = 50 # meter

samples,lidar_samples = Map.samples_scene(first, last)
ego_position = ego_pos(lidar_samples)

x = ego_position[0][0]
y = ego_position[0][1]

patch = ((x-10),(y-10),(x+10),(y+10))

grid = Grid(Map.minmax(x,y, LIDAR_RANGE))
Map.assign_layer(grid)
Visualise.show_grid(grid)
