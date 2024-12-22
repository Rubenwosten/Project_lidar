import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import Patch, Rectangle
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import ColorbarBase
from matplotlib.gridspec import GridSpec
import numpy as np
import os
from PIL import Image


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
    def show_layers(grid):
        """
        Visualizes the grid's layer matrix.

        Displays the layer grid and creates a legend for the different layers.
        """
        # Get the layer matrix
        layer_matrix = np.transpose(grid.get_layer_matrix())

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 8))

        flattened_layers = [layer for row in layer_matrix for layer in row]
        unique_layers = {layer for layer in flattened_layers if layer}

        # Create legend for the layer plot
        legend_handles = [Patch(color=Visualise.layer_colours.get(layer, 'white'), label=layer) for layer in unique_layers]

        # Create color matrix for layers
        color_matrix = np.array([
            [to_rgba(Visualise.layer_colours.get(layer, 'white')) for layer in row]
            for row in layer_matrix
        ])

        ax.imshow(color_matrix, origin='lower')
        ax.set_title("Layer Grid")
        ax.legend(handles=legend_handles, loc='upper right')

        plt.tight_layout()
        #plt.show()

        print('Layer grid visualization complete.')

    @staticmethod
    def show_risks(grid, index):
        """
        Displays a 2x2 subplot grid for risk matrices: Total Risk, Static Risk, Detect Risk, and Track Risk.

        :param grid: The grid object that holds the risk matrices.
        :param index: The index for the sample (used for dynamic risk calculations).
        """
        # Get matrices
        total_risk_matrix = np.transpose(grid.get_total_risk_matrix(index))
        static_risk_matrix = np.transpose(grid.get_static_risk_matrix())
        detect_risk_matrix = np.transpose(grid.get_detect_risk_matrix(index))
        track_risk_matrix = np.transpose(grid.get_track_risk_matrix(index))

        # Define the figure and 2x2 subplot layout
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))  # Adjusted figure size
        axes = axes.flatten()  # Flatten the 2x2 grid into a 1D array for easy iteration

        # Risk matrices and titles
        risk_matrices = {
            "Total Risk": total_risk_matrix,
            "Static Risk": static_risk_matrix,
            "Detect Risk": detect_risk_matrix,
            "Track Risk": track_risk_matrix,
        }

        for i, (title, matrix) in enumerate(risk_matrices.items()):
            ax = axes[i]
            im = ax.imshow(matrix, origin='lower', cmap='viridis', norm=Normalize(vmin=np.min(matrix), vmax=np.max(matrix)))
            ax.set_title(title, fontsize=12)

            # Disable gridlines for each subplot
            ax.grid(False)  # This removes the grid overlay
            
            # Add colorbar for each subplot
            cbar = fig.colorbar(ScalarMappable(norm=im.norm, cmap=im.cmap), ax=ax, shrink=0.8)
            cbar.set_label(title)

        # Adjust layout to avoid overlap
        plt.tight_layout(pad=5.0)  # Increase padding between subplots for better spacing
        #plt.show()

        #print('Risk grid visualization complete.')
    
    @staticmethod
    def show_risks_maximised(grid, index, max_total, max_static, max_detect, max_track):
        """
        Displays a 2x2 subplot grid for risk matrices: Total Risk, Static Risk, Detect Risk, and Track Risk.

        :param grid: The grid object that holds the risk matrices.
        :param index: The index for the sample (used for dynamic risk calculations).
        """
        # Get matrices
        total_risk_matrix = np.transpose(grid.get_total_risk_matrix(index))
        static_risk_matrix = np.transpose(grid.get_static_risk_matrix())
        detect_risk_matrix = np.transpose(grid.get_detect_risk_matrix(index))
        track_risk_matrix = np.transpose(grid.get_track_risk_matrix(index))

        # Define the figure and 2x2 subplot layout
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))  # Adjusted figure size
        axes = axes.flatten()  # Flatten the 2x2 grid into a 1D array for easy iteration

        # Risk matrices and titles
        risk_matrices = {
            "Total Risk": (total_risk_matrix, max_total),
            "Static Risk": (static_risk_matrix, max_static),  # Assuming static risk shares max_total
            "Detect Risk": (detect_risk_matrix, max_detect),
            "Track Risk": (track_risk_matrix, max_track),
        }

        for i, (title, (matrix, max_value)) in enumerate(risk_matrices.items()):
            ax = axes[i]
            norm = Normalize(vmin=0, vmax=max_value)
            im = ax.imshow(matrix, origin='lower', cmap='viridis', norm=norm)
            ax.set_title(title, fontsize=12)

            # Disable gridlines for each subplot
            ax.grid(False)  # This removes the grid overlay

            # Add colorbar for each subplot
            cbar = fig.colorbar(ScalarMappable(norm=im.norm, cmap=im.cmap), ax=ax, shrink=0.8)
            cbar.set_label(title)

        # Adjust layout to avoid overlap
        plt.tight_layout(pad=5.0)  # Increase padding between subplots for better spacing
        #plt.show()

        #print('Risk grid visualization complete.')

    @staticmethod
    def plot_grid(grid, index, prnt=False):
        """
        Visualizes the grid's layer and risk matrices in a combined layout:
        - Large plot for the layer grid.
        - 2x2 subplot grid for risk plots.
        """
        # Get matrices
        layer_matrix = np.transpose(grid.get_layer_matrix())
        total_risk_matrix = np.transpose(grid.get_total_risk_matrix(index))
        static_risk_matrix = np.transpose(grid.get_static_risk_matrix())
        detect_risk_matrix = np.transpose(grid.get_detect_risk_matrix(index))
        track_risk_matrix = np.transpose(grid.get_track_risk_matrix(index))

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
        #plt.show()

        print('Grid visualization complete.')

    @staticmethod
    def save_pointcloud_scatterplot(map, pointcloud, iteration, output_folder,overlay=True, total_size=8, dpi=100):
        """
        Creates and saves a scatter plot of the given point cloud.

        Parameters:
        - pointcloud: list of tuples [(x1, y1), (x2, y2), ...] representing lidar points.
        - iteration: int, the iteration number for naming the file.
        - output_folder: str, the directory where the scatter plot will be saved.
        """
        # Extract map bounds
        grid = map.grid
        ego_pos = map.ego_positions[iteration]

        x_min, x_max , y_min, y_max = grid.patch

        # Calculate aspect ratio
        aspect_ratio = grid.width / grid.length

        # Adjust figsize based on the aspect ratio
        if aspect_ratio >= 1:
            figsize = (total_size, total_size / aspect_ratio)  # Wide map
        else:
            figsize = (total_size * aspect_ratio, total_size)  # Tall map

        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Generate the scatter plot
        plt.figure(figsize=figsize,dpi=dpi)  # Adjust figure size as needed

        if overlay:
            # Get the layer matrix from the grid and plot it as the background
            layer_matrix = np.transpose(grid.get_layer_matrix())  # Assuming this gives a matrix of layers
            flattened_layers = [layer for row in layer_matrix for layer in row]
            unique_layers = {layer for layer in flattened_layers if layer}

            # Create the color matrix for the layer grid
            color_matrix = np.array([
                [to_rgba(Visualise.layer_colours.get(layer, 'white')) for layer in row]
                for row in layer_matrix
            ])

            # Display the layer grid as the background
            plt.imshow(color_matrix, origin='lower', extent=[0, grid.width, 0, grid.length])

        plt.scatter(
            [point[0] for point in pointcloud],  # X-coordinates
            [point[1] for point in pointcloud],  # Y-coordinates
            c='black', s=1, marker='.'  # Black points, small size, dot marker
        )

        # Plot the red box at the ego position
        ego_x, ego_y, _ = ego_pos
        ego_x, ego_y = (ego_x-x_min)/grid.res, (ego_y-y_min)/grid.res
        ego_box_size = 0.5  # Define the size of the red box (adjust as needed) In amount of cells covered (currently its a 5x5m box)
        red_box = Rectangle(
            (ego_x - ego_box_size / 2, ego_y - ego_box_size / 2),  # Bottom-left corner
            ego_box_size, ego_box_size,  # Width and height
            linewidth=2, edgecolor='red', facecolor='none'
        )
        plt.gca().add_patch(red_box)  # Add the red box to the plot

        # Set plot background to white
        plt.gca().set_facecolor('white')

        # Set axis limits to map dimensions
        plt.xlim(0, grid.width)
        plt.ylim(0, grid.length)

        # Configure plot aesthetics
        plt.gca().set_aspect('equal', adjustable='box')  # Ensure aspect ratio matches the map
        plt.title(f"Point Cloud Iteration {iteration}")
        plt.xlabel("X (Map Coordinates)")
        plt.ylabel("Y (Map Coordinates)")

        # Save the plot
        plot_filename = os.path.join(output_folder, f"pointcloud_iter_{iteration}.png")
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Point cloud scatter plot for iteration {iteration} saved as '{plot_filename}'.")

    def create_gif_from_folder(image_folder, output_gif_path, duration=500):
        """
        Creates and saves a GIF from a folder of images.
        
        Parameters:
        - image_folder: str, path to the folder containing the images.
        - output_gif_path: str, the path where the GIF will be saved.
        - duration: int, the duration for each frame in the GIF in milliseconds (default is 500ms).
        """
        # List all image files in the folder, sorted by file name (for correct ordering)
        image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])

        # Load all the images into a list
        images = []
        for image_file in image_files:
            img_path = os.path.join(image_folder, image_file)
            img = Image.open(img_path)
            images.append(img)

        # Save the images as a GIF
        images[0].save(
            output_gif_path, 
            save_all=True, 
            append_images=images[1:], 
            duration=duration, 
            loop=0  # Set loop to 0 for infinite loop, 1 for one-time animation
        )

        print(f"GIF saved as {output_gif_path}")