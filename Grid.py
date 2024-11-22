# This class creates a grid 
from Cell import Cell
import numpy as np

class Grid:

    def __init__(self, x_min, x_max , y_min, y_max, resolution):
   
        self.width = int((x_max - x_min)/resolution)
        self.length = int((y_max - y_min)/resolution)
        self.xarray = np.linspace(x_min, x_max, self.width)
        self.yarray = np.linspace(y_min, y_max, self.length)
        
        self.grid = [[Cell(x, y) for y in range(self.length)] for x in range(self.width)]

        print('grid of width {} and length {} was created'.format(self.width, self.length))
        
        