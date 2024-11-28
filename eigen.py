from nuscenes.nuscenes import NuScenes 
import matplotlib.pyplot as plt
import numpy as np

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

nusc_map = NuScenesMap(dataroot='C:/Users/Ruben/OneDrive/Bureaublad/data/sets/nuscenes/v1.0-mini', map_name='singapore-onenorth')
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
anns = Anns(samples[3])
print(anns[20])

static_layer_rasterizer = StaticLayerRasterizer(helper)
agent_rasterizer = AgentBoxesWithFadedHistory(helper, seconds_of_history=1)
mtp_input_representation = InputRepresentation(static_layer_rasterizer, agent_rasterizer, Rasterizer())

img = mtp_input_representation.make_input_representation(anns[1][1],samples[3])

backbone = ResNetBackbone('resnet50')
mtp = MTP(backbone, num_modes=6)

agent_state_vector = torch.Tensor([[helper.get_velocity_for_agent(anns[20][1], samples[3]),
                                    helper.get_acceleration_for_agent(anns[20][1], samples[3]),
                                    helper.get_heading_change_rate_for_agent(anns[20][1], samples[3])]])


image_tensor = torch.Tensor(img).permute(2, 0, 1).unsqueeze(0)

route = mtp(image_tensor, agent_state_vector)
print(route)
print(layers)
print(layers_2)