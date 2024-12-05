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
        
    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.length:
            return self.grid[x][y]
        else:
            raise IndexError(f"Cell coordinates ({x}, {y}) are out of bounds. "
                             f"Grid size is width={self.width}, length={self.length}.")

    def get_layer_matrix(self):
        """
        Returns a 2D matrix of layer values for visualization.
        """
        return [[cell.layer for cell in row] for row in self.grid]
    
    def to_dict(self):
        """
        Convert the Grid object into a dictionary format for saving.
        """
        # Include x_min, x_max, y_min, y_max, and resolution
        return {
            'x_min': self.xarray[0],
            'x_max': self.xarray[-1],
            'y_min': self.yarray[0],
            'y_max': self.yarray[-1],
            'resolution': (self.xarray[1] - self.xarray[0]) if len(self.xarray) > 1 else 1,
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
        # Extract necessary data to recreate the patch and resolution
        x_min = grid_dict['grid'][0][0]['x']  # First cell's x-coordinate
        x_max = grid_dict['grid'][-1][-1]['x']  # Last cell's x-coordinate
        y_min = grid_dict['grid'][0][0]['y']  # First cell's y-coordinate
        y_max = grid_dict['grid'][-1][-1]['y']  # Last cell's y-coordinate
        resolution = (x_max - x_min) / (grid_dict['width'] - 1)

        # Create the Grid object
        grid = Grid(patch=(x_min, x_max, y_min, y_max), resolution=resolution)

        # Restore other attributes
        grid.width = grid_dict['width']
        grid.length = grid_dict['length']
        grid.has_assigned_layers = grid_dict['has_assigned_layers']

        # Rebuild the grid with Cell objects
        grid.grid = [
            [Cell.from_dict(cell_dict) for cell_dict in row]
            for row in grid_dict['grid']
        ]

        return grid

        