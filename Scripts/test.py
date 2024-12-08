from Visualise import Visualise
from Map import Map
from Risk import Risk
import os
import matplotlib.pyplot as plt
from Severity import severity


LIDAR_RANGE = 50 # 50 meter
RESOLUTION = 10 # meter

#dataroot = r'C:/Users/marni/OneDrive/Documents/BEP 2024/data/sets/nuscenes'
dataroot = r'C:/Users/Chris/Python scripts/BEP VALDERS/data/sets/nuscenes'
map_name = 'boston-seaport' #'singapore-onenorth'

map_width = 2979.5
map_height = 2118.1

x = 360 # ego_position[0][0]
y = 1112 # ego_position[0][1]
ego = (x, y)

scene_id = 1

map = Map(dataroot, map_name, map_width, map_height, scene_id, LIDAR_RANGE, RESOLUTION)

filename = f'run boston scene {scene_id}\ boston scene {scene_id} res={RESOLUTION}'

if os.path.exists(filename):
    # Load the grid
    map.load_grid(filename)

    # Initialize risk calculation
    risk = Risk()

    # Create a folder to save the plots if it doesn't already exist
    run_folder = f"run {filename}"  # Include resolution in the plot folder name
    os.makedirs(run_folder, exist_ok=True)

    # Layer plot filename
    layer_plot_filename = os.path.join(run_folder, f"layer_plot_res={RESOLUTION}.png")
    Visualise.show_layers(map.grid)

    # Save the layer plot
    plt.savefig(layer_plot_filename)
    plt.close()
    print(f"Layer plot saved as '{layer_plot_filename}'.")

    # Calculate risk for each sample and save the plot
    for i, sample in enumerate(map.samples):
        # Calculate risk
        risk.CalcRisk(map, (1, 1, 1), i)

        # Risk plot filename
        risk_plot_filename = os.path.join(run_folder, f"risk_plot_iter_{i}_res={RESOLUTION}.png")
        Visualise.show_risks(map.grid, i)  # Show risks for the current iteration

        # Save the risk plot
        plt.savefig(risk_plot_filename)
        plt.close()  # Close the plot to free resources for the next iteration

        print(f"Risk plot for iteration {i} saved as '{risk_plot_filename}'.")
else:
    print(f"{filename} was not found")


severity.factor("vehicle.construction", "front", "front")

#Visualise.plot_grid(map.grid)
