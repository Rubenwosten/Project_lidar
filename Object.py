from nuscenes.nuscenes import NuScenes 
from Cell import Cell

import matplotlib.pyplot as plt
import numpy as np
import math

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

num_of_modes = 5
lengte = 24

class Object:
    def __init__(self,instancetoken, sampletoken, translation, rotation, size, catogory,reso ):
        #data object
        self._sample = None
        self.oud = None


        
        #nusc function
        self.reso=reso
        self.nusc = NuScenes(version='v1.0-mini', verbose=False)
        self.nusc_map = NuScenesMap(dataroot='C:/Users/Ruben/OneDrive/Bureaublad/data/sets/nuscenes/v1.0-mini', map_name='singapore-onenorth')
        self.helper = helper = PredictHelper(self.nusc)
        #Prediction function
        self.static_layer_rasterizer = StaticLayerRasterizer(helper)
        self.agent_rasterizer = AgentBoxesWithFadedHistory(helper, seconds_of_history=1)
        self.mtp_input_representation = InputRepresentation(self.static_layer_rasterizer, self.agent_rasterizer, Rasterizer())
        self.backbone = ResNetBackbone('resnet50')
        self.mtp = MTP(self.backbone, num_modes=num_of_modes)
        
    @property
    def sample(self):
        return self._sample
    
    @sample.setter
    def sample(self, samp):
        self._sample = samp
        if self._sample != self.oud:
            info = self.nusc.get('sample', self._sample)
            anns = info['anns']
            for i in range(len(anns)):
                ans = anns[i]
                info = self.nusc.get(('sample_annotation', ans))
                voor = self.voorspelling(ans)
                gespl , prob = self.route_splitser(num_of_modes,lengte, voor)
                j=0
                for j in range(num_of_modes):
                    box = self.bounding_box(info['size'], info['rotation'], gespl[2*i][0], gespl[2*i+1][0])
                    j+=1
                i+=1
                self.oud = samp
        else: return


    def voorspelling(self,objecttoken):
        img = self.mtp_input_representation.make_input_representation(objecttoken,self.sampletoken)
        agent_state_vector = torch.Tensor([[self.helper.get_velocity_for_agent(objecttoken, self.sampletoken),
                                    self.helper.get_acceleration_for_agent(objecttoken, self.sampletoken),
                                    self.helper.get_heading_change_rate_for_agent(objecttoken, self.sampletoken)]])
        image_tensor = torch.Tensor(img).permute(2, 0, 1).unsqueeze(0)
        voorspelling = self.mtp(image_tensor, agent_state_vector)
        return voorspelling
    
    def route_splitser(self, num_of_modes,route_length,voorspell):
        route_dim = (num_of_modes*2,route_length/2)
        route_tensor = voorspell.flatten()
        routestensor = route_tensor[:num_of_modes * route_length].view(-1)
        probabilities_tensor = route_tensor[num_of_modes * route_length:]
        
        gespilts = routestensor.view(num_of_modes, 2, -1).permute(1, 2, 0).reshape(int(route_dim[0]), int(route_dim[1])).detach().numpy()
        prob_logit = probabilities_tensor.detach().numpy()
        som = 0
        i = 0
        for i in range(num_of_modes):
            som += math.exp(prob_logit[i])
            i+=1
        i=0
        prob = np.empty(num_of_modes)
        for i in range(num_of_modes):
            prob[i] = math.exp(prob_logit[i])/som
            i +=1
        return gespilts, prob

    def risk_to_cell(self, box):
            j = np.min(box[:][0])
            while j!=np.max(box[:][0]):
                k = np.min(box[:][1])
                while k!=np.max(box[:][1]):
                    #cell.risk.trajactory(j,k)=1-self.prob[i]
                    k+=self.reso
                j+=self.reso
    
    def bounding_box(self, size, rotation, x, y):
        box = np.array([-0.5*size[0],-0.5*size[1]], [0.5*size[0],-0.5*size[1]], [-0.5*size[0],0.5*size[1]], [0.5*size[0],0.5*size[1]])
        rot = np.array([rotation[0],-rotation[1]],[rotation[1],rotation[0]])
        rotbox = np.dot(rot,box)
        rotbox = rotbox + np.array([x,y])
        return rotbox
    
