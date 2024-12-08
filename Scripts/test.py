from Visualise import Visualise
from Map import Map
from Risk import Risk
import os
import matplotlib.pyplot as plt
from Severity import severity
import pickle


LIDAR_RANGE = 50 # 50 meter
RESOLUTION = 10 # meter

#dataroot = r'C:/Users/marni/OneDrive/Documents/BEP 2024/data/sets/nuscenes'
dataroot = r'C:/Users/Chris/Python scripts/BEP VALDERS/data/sets/nuscenes'
map_name = 'boston-seaport' #'singapore-onenorth'

map_width = 2979.5
map_height = 2118.1

x = 600 # ego_position[0][0]
y = 1600 # ego_position[0][1]
ego = (x, y)

scene_id = 1

map = Map(dataroot, map_name, map_width, map_height, scene_id, LIDAR_RANGE, RESOLUTION)
'''
filepaths = [os.path.join('run boston scene 1 res = 10','boston scene 1 res = 10 data'),
             os.path.join('run boston scene 1 res = 5','boston scene 1 res = 5 data'),
             os.path.join('run boston scene 1 res = 2','boston scene 1 res = 2 data')]

for filepath in filepaths:
    map.grid = map.load_grid(filepath)
    print(map.grid.grid[0][0].occ)
    '''
res = 1
scene_id = 2
map.load_grid(os.path.join(f'run boston scene {scene_id} res = {res}',f'boston scene {scene_id} res = {res} data'))

print(map.grid.count_layers())