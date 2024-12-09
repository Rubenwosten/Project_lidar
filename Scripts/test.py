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

scene_ids = [0,1,2,3,4,5]
resolutions = [10, 5, 2, 1]
''' 
def add_lidar_aantal_to_saved_grid(filename):
    """
    Add a new field 'lidar_aantal' to each cell in a saved grid dictionary.
    The new field is an empty list of size 'scene_length'.
    """
    
    # Load the saved grid dictionary
    with open(filename, 'rb') as infile:
        grid_dict = pickle.load(infile)
    
    # Extract the scene length from the grid dictionary
    scene_length = grid_dict['scene length']
    
    # Add the 'lidar_aantal' field to each cell in the grid
    for row in grid_dict['grid']:
        for cell_dict in row:
            cell_dict['lidar_aantal'] = [0] * scene_length  # Initialize as an empty list of size scene_length
    
    # Save the updated grid dictionary
    with open(filename, 'wb') as outfile:
        pickle.dump(grid_dict, outfile)

    print(f"Updated grid with 'lidar_aantal' saved to {filename}")

for scene_id in scene_ids:
    for res in resolutions:
        filepath = os.path.join(f'run boston scene {scene_id} res = {res}', f'boston scene {scene_id} res = {res} data')
        if os.path.exists(filepath):
            map = Map(dataroot, map_name, map_width, map_height, scene_id, LIDAR_RANGE, res)

            map.load_grid(filepath)

            print(f"for file: {filepath} lidar_aantal = {map.grid.grid[0][0].lidar_aantal}")
        
    

map = Map(dataroot, map_name, map_width, map_height, scene_id, LIDAR_RANGE, 1)
filepath = os.path.join(f'run boston scene {1} res = {1}', f'boston scene {1} res = {1} data')
map.grid = map.load_grid(filepath)


filepaths = [f'run boston scene {scene_id} res = {res}'}

for filepath in filepaths:
    map = Map(dataroot, map_name, map_width, map_height, scene_id, LIDAR_RANGE, RESOLUTION)
    map.grid = map.load_grid(filepath)
    print(map.grid.grid[0][0].occ)
   
res = 1
scene_id = 2
map.load_grid(os.path.join(f'run boston scene {scene_id} res = {res}',f'boston scene {scene_id} res = {res} data'))

print(map.grid.count_layers()) 
'''



