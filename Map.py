
import numpy as np
import time
from tqdm import tqdm
from Grid import Grid
import pickle
import os

from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor

from nuscenes.nuscenes import NuScenes
from nuscenes.map_expansion.map_api import NuScenesMap
from nuscenes.map_expansion import arcline_path_utils
from nuscenes.map_expansion.bitmap import BitMap

def assign_layer_task(x, nusc_map, rec, grid, prnt=False):
    """
    This function processes a single row (x) of the grid and assigns layers to it.
    """
    row_results = []
    for y, _ in enumerate(grid.yarray):  # Process every column in the row
        layers = nusc_map.layers_on_point_v2(x, y, rec)
        row_results.append((x, y, layers))  # Append (x, y, layers) for each cell in the row
    return row_results  # Return results for the entire row


class Map:

    def __init__(self, dataroot, map_name, map_width, map_height, scene_id, RANGE, RES) -> None:
        # get the correct nuscenes object
        self.nusc = NuScenes(version='v1.0-mini', dataroot=dataroot, verbose=False)

        self.nusc_map = NuScenesMap(dataroot=dataroot, map_name=map_name)
        self.bitmap = BitMap(self.nusc_map.dataroot, self.nusc_map.map_name, 'basemap')

        # save the width and height of the map
        self.map_width = map_width
        self.map_height = map_height

        # get the specific scene based on the scene id 
        self.scene, first, last = self.get_scene(scene_id)

        # get the ego positions of the car for all samples of the scene
        self.samples,lidar_samples = self.samples_scene(first, last)
        self.ego_position = self.ego_pos(lidar_samples)

        # make a patch based on the min and max of the coordinates plus the range of the lidar
        self.patch = self.get_patch(self.ego_position, RANGE)
        print('patch = {}'.format(self.patch))

        #TODO add a bit of code that checks if the grid is saved, if so load up the grid

        # initialise a cell grid 
        self.grid = Grid(self.patch, RES)

        # get all records within your map
        self.rec = self.get_records_in_patch(self.patch)


    def get_scene(self, index):
        #sample array
        self.scene = self.nusc.scene[index]
        first = self.scene['first_sample_token']
        last = self.scene['last_sample_token']
        return self.scene, first, last

    # This function loads in each sample in the the scene
    # returns a numpy array of the samples and a numpy array of the lidar sample
    def samples_scene(self, first,last):
        samples = np.empty(0)
        lidar_sample = np.empty(0)
        sample = first

        while sample != last:
            samples = np.append(samples, sample)
            info = self.nusc.get('sample', sample)
            sample = info['next']
            lidar_sample = np.append(lidar_sample, info['data']['LIDAR_TOP'])
        samples = np.append(samples, last)
        info_last= self.nusc.get('sample', last)
        lidar_sample = np.append(lidar_sample, info_last['data']['LIDAR_TOP'])
        return samples,lidar_sample


    # This function determines the path of the ego vehicle
    # returns a numpy array of the ego vehicles position
    def ego_pos(self, lidar_samples):
        ego_trans = np.empty((40,3))
        i = 0
        for i in range(len(lidar_samples)):
            info = self.nusc.get('sample_data', lidar_samples[i])
            info_2 = self.nusc.get('ego_pose', info['ego_pose_token'])
            ego_trans[i] = info_2['translation']
            i += 1
        return ego_trans
        
    def minmax(self, x, y, range):
        x_min = np.min(x) - range
        x_max = np.max(x) + range
        y_min = np.min(y) - range
        y_max = np.max(y) + range
        return (x_min, x_max, y_min, y_max)

    def get_patch(self, ego, range):
        x_min = np.min(ego[:,0]) - range
        x_max = np.max(ego[:,0]) + range
        y_min = np.min(ego[:,1]) - range
        y_max = np.max(ego[:,1]) + range
        return (x_min, x_max, y_min, y_max)

    # This function changes the occurance values after each timestep
    # returns the new occurance grid
    def occurnence(self, occ, is_gescand, x, y, r,x_range,y_range ):
        occur = occ
        i = 0
        for i in range(x_range):
            j = 0
            for j in range(y_range):
                if ((i<(x-r)) or (i>(x+r)) or (j<(y-r)) or (j>(y+r))):
                    if occur[i][j] == 1:
                        occur[i][j]= occur[i][j] 
                    else: occur[i][j] += 0.25
                else:
                    if is_gescand[i-(x-r)][j-(y-r)] == 1:
                        occur[i][j] = 0
                    else:
                        if occur[i][j] == 1:
                            occur[i][j]= occur[i][j] 
                        else: occur[i][j] += 0.25 
                j+=1
            i+=1        
        return occur


    def gescand(self, occ, circle, x, y, r, x_range, y_range):
        is_gescand = np.zeros((2*r+1,2*r+1))
        i = 0
        for i in range (x_range):
            j = 0
            for j in range (y_range):
                if circle[i][j]==1:
                    if occ[i+x-r][j+y-r]>0.5:
                        is_gescand[i][j] = 1
                    else:
                        is_gescand[i][j] = 0
                else: is_gescand[i][j] = 0
                j += 1
            i+=1
        return is_gescand

    # This function determines what grid cells are of interest with respect to the ego position
    # This returns a 2d numpy array that is of size(r,r) with the grid cells in the circle having a value of 1 
    # and the grid cells outside of the circle having a value of 0
    def circle_of_interrest(self, r):
        circle = np.zeros((2*r+1,2*r+1))
        for i in range(2*r+1):
            a = pow((i - r),2)
            b = pow(r,2) - a
            if b > 0:
                y1 = round((r-np.sqrt(b)))
                y2 = round((r+np.sqrt(b)))
                j = 0
                for j in range(y2-y1):
                    circle[i][j+y1] = 1
                    j+=1
                i+=1
            elif b == 0:
                circle[i][r]= 1
                i+= 1
            else:
                circle[i]=circle[i]
                i+=1
        return circle



    def map_interrest(self, grid, x_range, y_range):
        map_int = grid
        i = 0
        for i in range(x_range):
            j = 0 
            for j in range(y_range):
                x = 10*i
                y = 10*j
                record = self.nusc_map.layers_on_point(x,y)
                if (record['drivable_area']!= '' or record['road_block']!= '' or record['road_segment']!= '' or record['lane']!= '' or record['ped_crossing']!= '' or record['stop_line']!= '' or record['carpark_area']!= '' or record['ped_crossing']!= ''):
                    map_int[i][j] = 1
                else: map_int[i][j] = 0
                j+=1
            i+=1
        return map_int

    # this function assigns the layers variable of each cell based on the records within the map
    def assign_layer(self, filename, prnt = False):
        if (self.grid.has_assigned_layers == False):
            elements = self.grid.width * self.grid.length
            time_per_element = 1 / 22.72795127375305
            print('assigning layers to the grid with {} elements'.format(elements))
            print('estimated time till completion = {} seconds'.format(elements * time_per_element))

            start_time = time.time()
            for i, x in enumerate(tqdm(self.grid.xarray)):
                if(prnt):
                    print('assigning for i = {} and x = {} at time = {}'.format(i, x, time.time() - start_time))
                for j, y in enumerate(self.grid.yarray):
                    self.grid.grid[i][j].layers = self.nusc_map.layers_on_point_v2(x, y, self.rec)
                    self.grid.grid[i][j].assign_layer(prnt = False)
            self.grid.has_assigned_layers = True

            print('elements per second = {}'.format(elements / (time.time() - start_time)))
            print('grid layers were assigned')
            self.save_grid(filename)
        else:
            print('grid already has assigned layers')


        
    def assign_layer_parallel(self, filename, prnt=False):
        if not self.grid.has_assigned_layers:
            elements = self.grid.width * self.grid.length
            time_per_element = 1 / 22.72795127375305
            print(f'Assigning layers to the grid with {elements} elements.')
            print(f'Estimating time: {elements * time_per_element} seconds')

            start_time = time.time()

            # Limit number of processes to the number of CPU cores (e.g., 4 or 8 cores)
            num_workers = min(8, os.cpu_count())  # Use a maximum of 8 workers

            # Function to process a single row
            def process_row(row_index, nusc_map, rec, grid, prnt=False):
                # Process the row (x = row_index) and return the results for that row
                return assign_layer_task(row_index, nusc_map, rec, grid, prnt)

            all_results = []
            with ProcessPoolExecutor(max_workers=num_workers) as executor:
                futures = []
                
                # Submit tasks for each row
                for i, x in enumerate(tqdm(self.grid.xarray, desc="Assigning Rows")):
                    futures.append(executor.submit(process_row, i, self.nusc_map, self.rec, self.grid, prnt))

                # Collect results from all tasks
                for future in tqdm(futures, desc="Assigning Layers", total=len(futures)):
                    row_results = future.result()  # Each future returns a list of (x, y, layers) for the row
                    all_results.extend(row_results)  # Merge row results

            # Once all results are gathered, apply them to the grid in a single pass
            for x, y, layers in all_results:
                self.grid.grid[x][y].layers = layers

            self.grid.has_assigned_layers = True
            print(f'Elements per second: {elements / (time.time() - start_time)}')
            print('Grid layers assigned.')

            self.save_grid(filename)
        else:
            print('Grid already has assigned layers')




    # this function getsall the records within the patch of the map
    def get_records_in_patch(self, patch):
        # my_patch = (300, 1000, 500, 1200)
        records_within_patch = self.nusc_map.get_records_in_patch(patch, self.nusc_map.non_geometric_layers, mode='intersect')
        rec = {}
        layer_names=['drivable_area', 'road_segment', 'road_block', 'lane', 'ped_crossing', 'walkway', 'stop_line', 'carpark_area']

        for layer in layer_names:
            rec[layer] = {}
            for record in records_within_patch[layer]:
                info = self.nusc_map.get(layer, record)
                rec[layer][record] = info
        return rec
    
    # Save the grid object
    def save_grid(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.grid.to_dict(), f)  # Save the grid's dictionary representation

    # Load the grid object
    def load_grid(self, filename):
        with open(filename, 'rb') as f:
            grid_dict = pickle.load(f)  # Load the dictionary from the file
            self.grid = Grid.from_dict(grid_dict)
            return self.grid # Reconstruct the grid from the dictionary

    

