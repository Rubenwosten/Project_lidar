from nuscenes.nuscenes import NuScenes 
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
        self.objecttoken = instancetoken
        self.sampletoken = sampletoken
        self.translation = translation
        self.rotation = rotation
        self.bounding = np.array([-0.5*size[0],-0.5*size[1]],[0.5*size[0],-0.5*size[1]],[-0.5*size[0],0.5*size[1]],[0.5*size[0],0.5*size[0]])
        self.rot = np.array([rotation[0],-rotation[1]],[rotation[1],rotation[0]])
        self.catogory = catogory
        self.risico = self.risk()
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
        self.voorspell = self.voorspelling()
        self.routes, self.prob = self.route_splitser(num_of_modes, lengte)
        
        
    def voorspelling(self):
        img = self.mtp_input_representation.make_input_representation(self.objecttoken,self.sampletoken)
        agent_state_vector = torch.Tensor([[self.helper.get_velocity_for_agent(self.objecttoken, self.sampletoken),
                                    self.helper.get_acceleration_for_agent(self.objecttoken, self.sampletoken),
                                    self.helper.get_heading_change_rate_for_agent(self.objecttoken, self.sampletoken)]])
        image_tensor = torch.Tensor(img).permute(2, 0, 1).unsqueeze(0)
        voorspelling = self.mtp(image_tensor, agent_state_vector)
        return voorspelling
    
    def route_splitser(self, num_of_modes,route_length):
        route_dim = (num_of_modes*2,route_length/2)
        route_tensor = self.voorspell.flatten()
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

    def risk_to_cell(self):
        Bound_normal_frame = np.dot(self.rot,self.bounding)
        for i in range(num_of_modes):
            pot_loc = np.array([self.routes[2*i][0],self.routes[2*i+1][0]])
            bound = Bound_normal_frame+pot_loc
            j = np.min(bound[:][0])
            while j!=np.max(bound[:][0]):
                k = np.min(bound[:][1])
                while k!=np.max(bound[:][1]):
                    #cell.risk.trajactory(j,k)=1-self.prob[i]
                    k+=self.reso
                j+=self.reso
            i+=1

        return