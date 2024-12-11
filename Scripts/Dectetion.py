from nuscenes.nuscenes import NuScenes 
import numpy as np
import os


class Detect:
    def __init__(self, map, dataroot,reso):
        self._sample=None
        self._x = None
        self._y = None
        self.patchxmin = map.patch[0]
        self.patchymin = map.patch[2]
        self.oud = None
        self.dataroot = dataroot
        self.nusc = map.nusc
        self.file = None
        self.map = map
        self._sampleindex = None
        self.ego = self.map.ego_positions
        self.reso = reso
        self.width = self.map.grid.width
        self.length = self.map.grid.length

    @property 
    def sample(self): #getter om sample aftelezen
        return self._sample
    
    @sample.setter
    def sample(self, values): #values is een tuple van sample ego_x en ego_y
        self._sample, self._sampleindex = values
        self._x = self.ego[self._sampleindex][0]
        self._y = self.ego[self._sampleindex][1]
        if self._sample != self.oud: # alleen runnen als sample veranderd
            self.file_get()
            print ("file complete")
            self.lidar_coor()
            print("lidar complete")
            self.update_occerence()
            self.update_risk()
            self.oud = self._sample # sample is helemaal gerund dus dit is de stopconditie
        else: return


    def file_get(self): #Deze functie zoekt het bestand van de lidar pointcloud die bij de sample hoort. Vervolgens wordt het volledige pad er naar toe gemaakt.
        info =  self.nusc.get('sample', self._sample)
        info_2 = self.nusc.get('sample_data',info['data']['LIDAR_TOP'])
        self.file = os.path.join(self.dataroot, info_2['filename'])
        

    def lidar_coor(self):#Deze functie Loopt door het bestand heen. Het bestand heeft per Lidar punt een x, y, z coordinaten en de channel index + reflectifity

        som = 0
        lidar_punt=0
        
        with open(self.file, "rb") as f:
            number = f.read(4)
            
            while number != b"":
                quo, rem = divmod(som,5) #omdat je alleen x en y wilt gebruiken en niet de andere dingen kijk je naar het residu van het item waar die op zit.
                if rem == 0: # als het residu = 0 heb je het x coordinaat en res = 1 is het y-coordinaat
                    
                    x = np.frombuffer(number, dtype=np.float32)
                    number = f.read(4) #leest de volgende bit
                    
                elif rem ==1:
                    np.frombuffer(number, dtype=np.float32)
                    y = np.frombuffer(number, dtype=np.float32)
                    x_frame = int((x+self._x-self.patchxmin)/self.reso)
                    y_frame = int((y+self._y-self.patchymin)/self.reso)
                    lidar_punt += 1
                    
                    
                    if (x_frame<0 or y_frame<0 or x_frame>= self.width or y_frame>=self.length):
                        number = f.read(4) #leest de volgende bit
                    else: 
                        self.map.grid.get_cell(x_frame,y_frame).lidar_aantal[self._sampleindex] +=1
                        number = f.read(4) #leest de volgende bit
                else:
                    number = f.read(4) #leest de volgende bit
                som +=1 # som houdt bij hoeveel items gelezen zijn.


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
                
                # Debugging statement (currently commented out):
                # If lidar points exceed 1, print the occurrence value for debugging purposes.
                # if lidar_punten > 1:
                #     print(f"werkt zeer goed {lidar_punten} occ = {occ} cell occ = {cell.occ[self._sampleindex]}")


    def update_risk(self):
        for row in self.map.grid.grid:
            for cell in row:
                if cell.layer == 'empty':
                    sev = 0
                else:sev = cell.severity_scores[cell.layer]
                cell.detect_risk[self._sampleindex] = sev * cell.occ[self._sampleindex]
             
