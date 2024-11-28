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
        self.objecttoken = instancetoken
        self.sampletoken = sampletoken
        self.translation = translation
        self.rotation = rotation
        self.size = size
        self.catogory = catogory
        
    def voorspelling(self):