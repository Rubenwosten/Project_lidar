# This class creates a grid 
from Cell import Cell
import numpy as np

class Grid:

    def __init__(self, patch, resolution):
   
        x_min, x_max , y_min, y_max = patch
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
    
    def to_dict(self):
        """
        Convert the Grid object into a dictionary format for saving.
        """
        return {
            'width': self.width,
            'length': self.length,
            'grid': [[cell.to_dict() for cell in row] for row in self.grid],  # Convert all cells to dictionaries
            'has_assigned_layers': self.has_assigned_layers
        }

    @staticmethod
    def from_dict(grid_dict):
        """
        Convert a dictionary back into a Grid object.
        """
        grid = Grid(x_min=0, x_max=0, y_min=0, y_max=0, resolution=0)  # Create an empty grid
        grid.width = grid_dict['width']
        grid.length = grid_dict['length']
        grid.has_assigned_layers = grid_dict['has_assigned_layers']
        # Rebuild the grid by creating cells from dictionaries
        grid.grid = [
            [Cell.from_dict(cell_dict) for cell_dict in row] 
            for row in grid_dict['grid']
        ]
        return grid

        