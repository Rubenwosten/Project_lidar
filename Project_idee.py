import matplotlib.pyplot as plt
import tqdm
import numpy as np
import re

from nuscenes.nuscenes import NuScenes
from nuscenes.map_expansion.map_api import NuScenesMap
from nuscenes.map_expansion import arcline_path_utils
from nuscenes.map_expansion.bitmap import BitMap
 
nusc = NuScenes(version='v1.0-mini', verbose=False)

nusc_map = NuScenesMap(dataroot='C:/Users/Ruben/OneDrive/Bureaublad/data/sets/nuscenes/v1.0-mini', map_name='singapore-onenorth')
bitmap = BitMap(nusc_map.dataroot, nusc_map.map_name, 'basemap')

x_c = 270
y_c = 750
layer = nusc_map.layers_on_point(x_c,y_c)
if layer['ped_crossing'] == '':
    print('hoi')
else: print('gefaald')

map_width = 2979.5
map_height = 2118.1
#sample array
scene = nusc.scene[1]
first = scene['first_sample_token']
last = scene['last_sample_token']

# This function loads in each sample in the the scene
# returns a numpy array of the samples and a numpy array of the lidar sample
def samples_scene(first,last):
    samples = np.empty(0)
    lidar_sample = np.empty(0)
    sample = first

    while sample != last:
        samples = np.append(samples, sample)
        info = nusc.get('sample', sample)
        sample = info['next']
        lidar_sample = np.append(lidar_sample, info['data']['LIDAR_TOP'])
    samples = np.append(samples, last)
    info_last= nusc.get('sample', last)
    lidar_sample = np.append(lidar_sample, info_last['data']['LIDAR_TOP'])
    return samples,lidar_sample

# This function determines the path of the ego vehicle
# returns a numpy array of the ego vehicles position
def ego_pos(lidar_samples):
    ego_trans = np.empty((40,3))
    i = 0
    for i in range(len(lidar_samples)):
        info = nusc.get('sample_data', lidar_samples[i])
        info_2 = nusc.get('ego_pose', info['ego_pose_token'])
        ego_trans[i] = info_2['translation']
        i += 1
    return ego_trans
    
# This function determines the minimal and maximal values of the 
def minmax (x,y):
    x_min = np.min(x) - 50
    x_max = np.max(x) + 50
    y_min = np.min(y) - 50
    y_max = np.max(y) + 50
    return x_min, x_max, y_min, y_max

def grid(x_min, x_max , y_min, y_max):
   
    x_grid = (x_max - x_min)*10
    y_grid = (y_max - y_min)*10
    xarray = np.linspace(x_min, x_max, x_grid)
    yarray = np.linspace(y_min, y_max, y_grid)
    grid = np.empty((x_grid,y_grid))
    return grid, xarray, yarray

def risk():
    return

def circle_of_interrest(r):
    circle = np.zeros((2*r+1,2*r+1))
    for i in range(2*r+1):
        a = pow((i - r),2)
        b = pow(r,2) - a
        if b > 0:
            y1 = round((r-np.sqrt(b)))
            y2 = round((r+np.sqrt(b)))
            j = 0
            for j in range(y2-y1):
                circle[i][j+y1] = 1
                j+=1
            i+=1
        elif b == 0:
            circle[i][r]= 1
            i+= 1
        else:
            circle[i]=circle[i]
            i+=1
    return circle

def occurnence(occ, is_gescand, x, y, r,x_range,y_range ):
    occur = occ
    i = 0
    for i in range(x_range):
        j = 0
        for j in range(y_range):
            if ((i<(x-r)) or (i>(x+r)) or (j<(y-r)) or (j>(y+r))):
                if occur[i][j] == 1:
                    occur[i][j]= occur[i][j] 
                else: occur[i][j] += 0.25
            else:
                if is_gescand[i-(x-r)][j-(y-r)] == 1:
                    occur[i][j] = 0
                else:
                    if occur[i][j] == 1:
                        occur[i][j]= occur[i][j] 
                    else: occur[i][j] += 0.25 
            j+=1
        i+=1        
    return occur

def map_interrest(grid, x_range, y_range):
    map_int = grid
    i = 0
    for i in range(x_range):
        j = 0 
        for j in range(y_range):
            x = 10*i
            y = 10*j
            record = nusc_map.layers_on_point(x,y)
            if (record['drivable_area']!= '' or record['road_block']!= '' or record['road_segment']!= '' or record['lane']!= '' or record['ped_crossing']!= '' or record['stop_line']!= '' or record['carpark_area']!= '' or record['ped_crossing']!= ''):
                map_int[i][j] = 1
            else: map_int[i][j] = 0
            j+=1
        i+=1
    return map_int

def gescand(occ, circle, x, y, r, x_range, y_range):
    is_gescand = np.zeros((2*r+1,2*r+1))
    i = 0
    for i in range (x_range):
        j = 0
        for j in range (y_range):
            if circle[i][j]==1:
                if occ[i+x-r][j+y-r]>0.5:
                    is_gescand[i][j] = 1
                else:
                    is_gescand[i][j] = 0
            else: is_gescand[i][j] = 0
            j += 1
        i+=1
    return is_gescand

def static():
    return

def dynamic():
    return

def object_list():
    return

        

samples,lidar_samples = samples_scene(first, last)
ego_position = ego_pos(lidar_samples)

x = ego_position[0][0]
y = ego_position[0][1]

patch = ((x-10),(y-10),(x+10),(y+10))

