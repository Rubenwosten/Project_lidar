# This class creates a grid 
from Cell import Cell
import numpy as np

class Grid:

    def __init__(self, x_min, x_max , y_min, y_max, resolution):
   
        self.width = int((x_max - x_min)/resolution)
        self.length = int((y_max - y_min)/resolution)
        self.xarray = np.linspace(x_min, x_max, self.width)
        self.yarray = np.linspace(y_min, y_max, self.length)
        
        self.grid = [[Cell(self.xarray[x], self.yarray[y]) for y in range(self.length)] for x in range(self.width)]

        self.has_assigned_layers = False
        print('grid of width {} and length {} was created with {} elements'.format(self.width, self.length, self.width * self.length))
        
    def get_layer_matrix(self):
        """
        Returns a 2D matrix of layer values for visualization.
        """
        return [[cell.layer for cell in row] for row in self.grid]
        