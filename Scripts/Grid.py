# This class creates a grid 
from Cell import Cell
import numpy as np
import math

class Grid:

    def __init__(self, patch, resolution, scene_length, prnt=False):
        self.patch = patch 
        x_min, x_max , y_min, y_max = patch
        self.res = resolution
        self.scene_length = scene_length
        self.width = int((x_max - x_min)/resolution)
        self.length = int((y_max - y_min)/resolution)
        self.xarray = np.linspace(x_min, x_max, self.width)
        self.yarray = np.linspace(y_min, y_max, self.length)
        
        self.grid = [[Cell(self.xarray[x], self.yarray[y], scene_length) for y in range(self.length)] for x in range(self.width)]

        self.has_assigned_layers = False
        if prnt:
            print('grid of width {} and length {} was created with {} elements'.format(self.width, self.length, self.width * self.length))
        
    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.length:
            return self.grid[x][y]
        else:
            raise IndexError(f"Cell coordinates ({x}, {y}) are out of bounds. "
                             f"Grid size is width={self.width}, length={self.length}.")
    
    def count_layers(self):
        """
        Count the occurrences of each layer type in the grid.

        :return: Dictionary with layer names as keys and their counts as values
        """
        layer_counts = {layer: 0 for layer in Cell.priority_layers}

        for row in self.grid:
            for cell in row:
                for layer_name in cell.layers:
                    if layer_name in layer_counts:
                        layer_counts[layer_name] += 1

        return layer_counts
    
    def get_layer_matrix(self):
        return [[cell.layer for cell in row] for row in self.grid]
    
    def get_total_risk_matrix(self, i):
        return [[cell.total_risk[i] for cell in row] for row in self.grid]
    
    def get_static_risk_matrix(self):
        return [[cell.static_risk for cell in row] for row in self.grid]
    
    def get_detect_risk_matrix(self, i):
        return [[cell.detect_risk[i] for cell in row] for row in self.grid]
    
    def get_track_risk_matrix(self, i):
        return [[cell.track_risk[i] for cell in row] for row in self.grid]

    def to_dict(self):
        """
        Convert the Grid object into a dictionary format for saving.
        """
        return {
            'patch': self.patch,
            'resolution': self.res,
            'scene length': self.scene_length,
            'width': self.width,
            'length': self.length,
            'grid': [[cell.to_dict() for cell in row] for row in self.grid],  # Convert all cells to dictionaries
            'has_assigned_layers': self.has_assigned_layers
        }
    def circle_of_interrest(self, range, ego):
        circle_interrest = []
        for row in self.grid:
            for cell in row:
                x= cell.x
                y= cell.y
                distance = math.sqrt((y-ego[1])**2 + (x-ego[0])**2)
                if distance < range:
                    circle_interrest.append(cell)


    @staticmethod
    def from_dict(grid_dict):
        """
        Convert a dictionary back into a Grid object.
        """
        # Extract original patch and resolution
        patch = grid_dict['patch']
        resolution = grid_dict['resolution']
        scene_length = grid_dict['scene length']
        # Recreate the Grid object with the exact same patch and resolution
        grid = Grid(patch=patch, resolution=resolution, scene_length=scene_length)

        # Restore other attributes
        grid.width = grid_dict['width']
        grid.length = grid_dict['length']
        grid.has_assigned_layers = grid_dict['has_assigned_layers']
        # Rebuild the grid with Cell objects
        grid.grid = [
            [Cell.from_dict(cell_dict, scene_length) for cell_dict in row]
            for row in grid_dict['grid']
        ]

        return grid

        