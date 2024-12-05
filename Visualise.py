import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import Patch
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import ColorbarBase
from matplotlib.gridspec import GridSpec
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
    def plot_grid(grid, prnt=False):
        """
        Visualizes the grid's layer and risk matrices in a combined layout:
        - Large plot for the layer grid.
        - 2x2 subplot grid for risk plots.
        """
        # Get matrices
        layer_matrix = np.transpose(grid.get_layer_matrix())
        total_risk_matrix = np.transpose(grid.get_total_risk_matrix())
        static_risk_matrix = np.transpose(grid.get_static_risk_matrix())
        detect_risk_matrix = np.transpose(grid.get_detect_risk_matrix())
        track_risk_matrix = np.transpose(grid.get_track_risk_matrix())

        # Define the figure and gridspec layout
        fig = plt.figure(figsize=(18, 12))  # Adjust figure size
        gs = GridSpec(2, 3, figure=fig, width_ratios=[2, 1, 1])  # Define a 2x3 grid layout with custom width ratios

        # Large plot for layer grid (spanning 2 rows and 2 columns)
        ax1 = fig.add_subplot(gs[:, 0])  # Span both rows in the first column (left side)
        
        flattened_layers = [layer for row in layer_matrix for layer in row]
        unique_layers = {layer for layer in flattened_layers if layer}

        # Create legend for layer plot
        legend_handles = [Patch(color=Visualise.layer_colours.get(layer, 'white'), label=layer) for layer in unique_layers]

        # Create color matrix for layers
        color_matrix = np.array([
            [to_rgba(Visualise.layer_colours.get(layer, 'white')) for layer in row]
            for row in layer_matrix
        ])

        ax1.imshow(color_matrix, origin='lower')
        ax1.set_title("Layer Grid")
        ax1.legend(handles=legend_handles, loc='upper right')

        # Risk plots (2x2 grid in the remaining space)
        risk_matrices = {
            "Total Risk": total_risk_matrix,
            "Static Risk": static_risk_matrix,
            "Detect Risk": detect_risk_matrix,
            "Track Risk": track_risk_matrix,
        }

        for i, (title, matrix) in enumerate(risk_matrices.items()):
            # Determine subplot grid position (2x2 right-side subplots)
            ax = fig.add_subplot(gs[i//2, i%2 + 1])  # First row for 0,1 -> second row for 2,3 (right side)
            im = ax.imshow(matrix, origin='lower', cmap='viridis', norm=Normalize(vmin=np.min(matrix), vmax=np.max(matrix)))
            ax.set_title(title)

            # Add colorbar for each subplot
            cbar = fig.colorbar(ScalarMappable(norm=im.norm, cmap=im.cmap), ax=ax)
            cbar.set_label(title)

        plt.tight_layout()
        plt.show()

        print('Grid visualization complete.')
