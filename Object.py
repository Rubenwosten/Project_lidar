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


class Object:
    def __init__(self,instancetoken, sampletoken, translation, rotation, size, catogory ):
        #data object
        self.objecttoken = instancetoken
        self.sampletoken = sampletoken
        self.translation = translation
        self.rotation = rotation
        self.size = size
        self.catogory = catogory
        #nusc function
        self.nusc = NuScenes(version='v1.0-mini', verbose=False)
        self.nusc_map = NuScenesMap(dataroot='C:/Users/Ruben/OneDrive/Bureaublad/data/sets/nuscenes/v1.0-mini', map_name='singapore-onenorth')
        self.helper = helper = PredictHelper(self.nusc)
        #Prediction function
        self.static_layer_rasterizer = StaticLayerRasterizer(helper)
        self.agent_rasterizer = AgentBoxesWithFadedHistory(helper, seconds_of_history=1)
        self.mtp_input_representation = InputRepresentation(self.static_layer_rasterizer, self.agent_rasterizer, Rasterizer())
        self.backbone = ResNetBackbone('resnet50')
        self.mtp = MTP(self.backbone, num_modes=6)
        
    def voorspelling(self):
        img = self.mtp_input_representation.make_input_representation(self.objecttoken,self.sampletoken)
        agent_state_vector = torch.Tensor([[self.helper.get_velocity_for_agent(self.objecttoken, self.sampletoken),
                                    self.helper.get_acceleration_for_agent(self.objecttoken, self.sampletoken),
                                    self.helper.get_heading_change_rate_for_agent(self.objecttoken, self.sampletoken)]])
        image_tensor = torch.Tensor(img).permute(2, 0, 1).unsqueeze(0)
        voorspelling = self.mtp(image_tensor, agent_state_vector)
        return voorspelling