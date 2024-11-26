import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import Patch
import numpy as np

class Visualise:

    layer_names = ['polygon', 'line', 'node', 'drivable_area', 'road_segment', 'road_block', 'lane', 'ped_crossing', 'walkway', 
                   'stop_line', 'carpark_area', 'lane_connector', 'road_divider', 'lane_divider', 'traffic_light']

    non_geometric_polygon_layers = ['drivable_area', 'road_segment', 'road_block', 'lane', 'ped_crossing',
                                             'walkway', 'stop_line', 'carpark_area']

    layer_colours = {
        'empty': 'white',
        'drivable_area': 'green',
        'road_segment': 'brown',
        'road_block': 'darkred',
        'lane': 'yellow',
        'ped_crossing': 'orange',
        'walkway': 'tan',
        'stop_line': 'red',
        'carpark_area': 'lightblue'
    }


    @staticmethod
    def plot_grid(grid, prnt = False):
        """
        Visualizes the grid's layer variable as a grid plot.
        :param grid: A Grid object to visualize
        """
        layer_matrix = grid.get_layer_matrix()
        if(prnt):
            print("Layer Matrix: \n{}".format(layer_matrix))
        # Flatten the layer_matrix to get the unique layers
        flattened_layers = [layer for row in layer_matrix for layer in row]
        unique_layers = {layer for layer in flattened_layers if layer}

        # Create the legend handles using the unique layers
        legend_handles = [Patch(color=Visualise.layer_colours[layer], label=layer) for layer in unique_layers]

        # Create a color matrix based on the layer_colours dictionary
        color_matrix = np.array([
            [to_rgba(Visualise.layer_colours.get(layer, 'white')) for layer in row]  # Default to white for undefined layers
            for row in layer_matrix
        ])

        # Use matplotlib to plot the grid
        plt.figure(figsize=(8, 8))
        plt.imshow(color_matrix, origin='upper')
        plt.title("Grid Visualization with Layer Colors")
        plt.legend(handles=legend_handles, loc='upper right')
        #plt.axis("off")  # Turn off axes for better visualization
        plt.show()

        print('grid was visualised')
