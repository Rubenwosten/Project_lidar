from Visualise import Visualise
from Map import Map

LIDAR_RANGE = 5 # 50 meter
RESOLUTION = 1 # meter

dataroot = r'C:/Users/Chris/Python scripts/BEP VALDERS/data/sets/nuscenes'
map_name = 'singapore-onenorth'

map_width = 2979.5
map_height = 2118.1

x = 360 # ego_position[0][0]
y = 1112 # ego_position[0][1]
ego = (x, y)

scene_id = 1

map = Map(dataroot, map_name, map_width, map_height, scene_id, LIDAR_RANGE, RESOLUTION)

filename = 'layer map boston scene 1 high res'

map.load_grid(filename)

Visualise.plot_grid(map.grid)