from nuscenes.nuscenes import NuScenes 
import matplotlib.pyplot as plt
import numpy as np
import math 
import os

from nuscenes.map_expansion.map_api import NuScenesMap
from nuscenes.map_expansion import arcline_path_utils
from nuscenes.map_expansion.bitmap import BitMap
from nuscenes.eval.prediction.splits import get_prediction_challenge_split
from nuscenes.prediction import PredictHelper

from nuscenes.prediction.input_representation.static_layers import StaticLayerRasterizer
from nuscenes.prediction.input_representation.agents import AgentBoxesWithFadedHistory
from nuscenes.prediction.input_representation.interface import InputRepresentation
from nuscenes.prediction.input_representation.combinators import Rasterizer

from nuscenes.prediction.models.backbone import ResNetBackbone
from nuscenes.prediction.models.mtp import MTP
from nuscenes.prediction.models.covernet import CoverNet
import torch


nusc = NuScenes(version='v1.0-mini', verbose=False)
dataroot='C:/Users/Ruben/OneDrive/Bureaublad/data/sets/nuscenes'
nusc_map = NuScenesMap(dataroot='C:/Users/Ruben/OneDrive/Bureaublad/data/sets/nuscenes', map_name='singapore-onenorth')
bitmap = BitMap(nusc_map.dataroot, nusc_map.map_name, 'basemap')

helper = PredictHelper(nusc)

scene = nusc.scene[1]
first = scene['first_sample_token']
last = scene['last_sample_token']

my_patch = (300, 1000, 500, 1200)
records_within_patch = nusc_map.get_records_in_patch(my_patch, nusc_map.non_geometric_layers, mode='intersect')
rec = {}
layer_names=['drivable_area', 'road_segment', 'road_block', 'lane', 'ped_crossing', 'walkway', 'stop_line', 'carpark_area']

for layer in layer_names:
    rec[layer] = {}
    for record in records_within_patch[layer]:
        info = nusc_map.get(layer, record)
        rec[layer][record] = info

item = rec['lane']['03c94004-f3e2-4b92-87cb-5b57fa6ebe73']['polygon_token']

my_point = (390, 1100)
layers = nusc_map.layers_on_point_v2(my_point[0], my_point[1],rec)
layers_2 = nusc_map.layers_on_point(my_point[0],my_point[1])




def samples_scene(first,last):
    samples = np.empty(0)
    sample = first
    while sample != last:
        samples = np.append(samples, sample)
        info = nusc.get('sample', sample)
        sample = info['next']   
    samples = np.append(samples, last)
    
    return samples

def Anns(sample):
    info = nusc.get('sample', sample)
    anns = info['anns']
    anns_Move = []
    i = 0
    for i in range(len(anns)):
        token = anns[i]
        info = nusc.get('sample_annotation', token)
        inst = info['instance_token']
        cato = info['category_name']
        anns_Move.append([token,inst,cato])
        i += 1
    return anns_Move

samples = samples_scene(first, last)
info = nusc.get('sample', samples[0])
anns = info['anns']
a = anns[0]
info = nusc.get('sample_annotation', a)
print (info)

lidar_info =nusc.calibrated_sensor[5]
h= 1.84023
R = np.empty(24)
for i in range(len(R)):
    theta = (i*1.25 -30)/180
    R[i]= h*math.tan(theta)

scan = np.empty(36)
for i in range(len(scan)):
    phi = i*10
    for j in range(10):
        phi+=j
        phi = phi/180


info =  nusc.get('sample', first)
info_2 = nusc.get('sample_data',info['data']['LIDAR_TOP'])
file = os.path.join(dataroot, info_2['filename'])
print(file)
print(type(file))

som = 0
lidar_punt=0
            
with open(file, "rb") as f:
    number = f.read(4)
    print (number)
    while number != b"":
        quo, rem = divmod(som,5)
        if rem == 0:
            x = np.frombuffer(number, dtype=np.float32)
        elif rem ==1:
            y = np.frombuffer(number, dtype=np.float32)
            lidar_punt += 1
        number = f.read(4)
        print (number)
        som +=1
print (som)



R = 10
dt = 10
dt_rad = dt/180
x= 0
reso = 1
theta = 0
riskcones = np.empty(360/dt)
total_risk = 0
for i in range(360/dt):
    while x < R:
        if (theta>= -0.5*np.pi and theta<0.5*np.pi):
            a= 1
        else: a= -1
        y1 = x*np.tan(theta)
        y2 = x*np.tan(theta)
        if y2 < y1:
            ymin = y2
            ymax = y1
        else:
            ymin = y1
            ymax = y2
        while ymin < ymax:
            risk = risk.cell(a*x, ymin)
            riskcones[i] += risk
            total_risk += risk

for i in range(len(riskcones)):
    


    