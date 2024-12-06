from nuscenes.nuscenes import NuScenes 
import numpy as np
import os


class Detect:
    def __init__(self, map, dataroot):
        self._sample=None
        self.oud = None
        self.dataroot = dataroot
        self.nusc = NuScenes(version='v1.0-mini', verbose=False)
        self.file = None
        self.map = map

    @property
    def sample(self):
        return self._sample
    
    @sample.setter
    def sample(self, samp):
        self._sample = samp
        if self._sample != self.oud:
            self.file_get()
            self.lidar_coor()
            self.oud = samp
        else: return


    def file_get(self):
        info =  self.nusc.get('sample', self._sample)
        info_2 = self.nusc.get('sample_data',info['data']['LIDAR_TOP'])
        self.file = os.path.join(self.dataroot, info_2['filename'])
        print(type(self.file))

    def lidar_coor(self):
        som = 0
        lidar_punt=0
        
        with open(self.file, "rb") as f:
            number = f.read(4)
            print (number)
            while number != b"":
                quo, rem = divmod(som,5)
                if rem == 0:
                    x = np.frombuffer(number, dtype=np.float32)
                elif rem ==1:
                    y = np.frombuffer(number, dtype=np.float32)
                    lidar_punt += 1
                    self.map.grid.get_cell(x,y).lidar_aantal +=1
                number = f.read(4)
                print(number)
                print(lidar_punt)
                som +=1
        print (som)