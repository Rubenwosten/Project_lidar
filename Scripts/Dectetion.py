from nuscenes.nuscenes import NuScenes 
import numpy as np
import os
from Visualise import Visualise

class Detect:
    def __init__(self, map):
        self._sample=None
        self._x = None
        self._y = None
        self.patchxmin = map.patch[0]
        self.patchymin = map.patch[2]
        self.oud = None
        self.dataroot = map.dataroot
        self.nusc = map.nusc
        self.file = None
        self.map = map
        self._sampleindex = None
        self.ego = self.map.ego_positions
        self.reso = map.grid.res
        self.lidarpoint = []
        self.lidarpointV2 = []
        self.width = self.map.grid.width
        self.length = self.map.grid.length

    @property 
    def sample(self): #getter om sample aftelezen
        return self._sample
    
    #@sample.setter
    #def sample(self, values): #values is een tuple van sample ego_x en ego_y
        

    def update(self, sample, sample_index, prnt=False):
        self._sample = sample
        self._sampleindex = sample_index
        self._x = self.ego[self._sampleindex][0]
        self._y = self.ego[self._sampleindex][1]
        
        if self._sample != self.oud: # alleen runnen als sample veranderd
            self.lidarpoint = []
            self.lidarpointV2 = []
            self.file_get()
            if prnt:
                print ("file complete")
            info = self.nusc.get('sample', self._sample)
            info = self.nusc.get('sample_data', info['data']['LIDAR_TOP'])
            info_2 = self.nusc.get('ego_pose', info['ego_pose_token'])
            rot = np.arctan2((2*(info_2['rotation'][0]*info_2['rotation'][3]+info_2['rotation'][1]*info_2['rotation'][2])),(1-2*(info_2['rotation'][3]**2+info_2['rotation'][2]**2)))
            if prnt:
                print (rot)
            rot_matrix = np.array([[np.cos(rot), np.sin(rot)], [-np.sin(rot), np.cos(rot)]])
            self.lidar_coor(rot_matrix)
            if prnt:
                print("lidar complete")
            self.update_occerence()
            self.update_risk()
            if prnt:
                print('self.lidarpoint[1] = ', self.lidarpoint[1])
                print('self.lidarpoint[1][1] = ', self.lidarpoint[1][1])
                print('self.lidarpoint[1][0] = ', self.lidarpoint[1][0])
            self.oud = self._sample # sample is helemaal gerund dus dit is de stopconditie
            return
        else: 
            return


    def file_get(self): #Deze functie zoekt het bestand van de lidar pointcloud die bij de sample hoort. Vervolgens wordt het volledige pad er naar toe gemaakt.
        info =  self.nusc.get('sample', self._sample)
        info_2 = self.nusc.get('sample_data',info['data']['LIDAR_TOP'])
        self.file = os.path.join(self.dataroot, info_2['filename'])
        

    def lidar_coor(self, rot_matrix):
        # Deze functie Loopt door het bestand heen. Het bestand heeft per Lidar punt een x, y, z coordinaten en de channel index + reflectifity
        som = 0
        lidar_punt = 0

        with open(self.file, "rb") as f:
            number = f.read(4)

            while number != b"":
                quo, rem = divmod(som, 5)  # omdat je alleen x, y, z wilt gebruiken kijk je naar het residu van het item waar die op zit.

                if rem == 0:  # residu = 0 -> x-coordinaat
                    x = np.frombuffer(number, dtype=np.float32)[0]
                    number = f.read(4)  # leest de volgende bit
                elif rem == 1:  # residu = 1 -> y-coordinaat
                    y = np.frombuffer(number, dtype=np.float32)[0]
                    number = f.read(4)  # leest de volgende bit
                elif rem == 2:  # residu = 2 -> z-coordinaat
                    z = np.frombuffer(number, dtype=np.float32)[0]
                    self.lidarpointV2.append((x, y, z))

                    xy= np.array([x,y])
                    xy_rotated = np.dot(rot_matrix, xy)
                    x_frame = (xy_rotated[0]+self._x-self.patchxmin)/self.reso
                    y_frame = (xy_rotated[1]+self._y-self.patchymin)/self.reso
                    self.lidarpoint.append((x_frame,y_frame))

                    x_frame = int(x_frame)
                    y_frame = int(y_frame)
                    lidar_punt += 1

                    x_global = x + self._x
                    y_global = y + self._y

                    if (
                        x_frame < 0
                        or y_frame < 0
                        or x_frame >= self.width
                        or y_frame >= self.length
                    ):
                        number = f.read(4)  # leest de volgende bit
                    else:
                        self.map.grid.get_cell(x_frame, y_frame).lidar_aantal[
                            self._sampleindex
                        ] += 1
                        number = f.read(4)  # leest de volgende bit
                else:
                    number = f.read(4)  # leest de volgende bit

                som += 1  # som houdt bij hoeveel items gelezen zijn.

        # print(lidar_punt)
        # print(som)


    def update_occerence(self):
        """
        Updates the occurrence (`occ`) value for each cell in the map grid 
        based on lidar data and occurrence accumulation/decay factors.
        """
        # Iterate through each row of the grid
        for row in self.map.grid.grid:
            # Iterate through each cell in the current row
            for cell in row:
                # Retrieve the lidar count for the current sample index
                lidar_punten = cell.lidar_aantal[self._sampleindex]
                
                # Determine the base occurrence (`occ`) value to update
                if self._sampleindex == 0:
                    # For the first sample index, use the current occurrence
                    occ = cell.occ[self._sampleindex]
                else:
                    # For subsequent indices, use the occurrence from the previous index
                    occ = cell.occ[self._sampleindex - 1]
                
                # Add the standard occurrence accumulation
                occ += self.map.OCC_ACCUM
                
                # Decay the occurrence based on lidar points and clamp it between 0 and 1
                occ = max(0, min(occ - self.map.LIDAR_DECAY * lidar_punten, 1))
                
                # Update the occurrence value for the current sample index in the cell
                cell.occ[self._sampleindex] = occ

    def update_risk(self):
        for row in self.map.grid.grid:
            for cell in row:
                if cell.layer == 'empty':
                    sev = 0
                else:sev = cell.severity_scores[cell.layer]
                cell.detect_risk[self._sampleindex] = sev * cell.occ[self._sampleindex]
             
