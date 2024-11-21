# This class creates a grid 
import Cell
import numpy as np

class Grid:

    def __init__(self, x_min, x_max , y_min, y_max, resolution):
   
        self.width = (x_max - x_min)*resolution
        self.length = (y_max - y_min)*resolution
        self.xarray = np.linspace(x_min, x_max, self.width)
        self.yarray = np.linspace(y_min, y_max, self.length)
        
        self.grid = [[Cell(x, y) for y in range(self.length)] for x in range(self.width)]
        
        