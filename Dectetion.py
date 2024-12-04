from nuscenes.nuscenes import NuScenes 
import numpy as np

class detect():
    def __init__(self, sample,):
        self.sample=sample
        self.nusc = NuScenes(version='v1.0-mini', verbose=False)
        self.file = self.file_get()


    def file_get(self):
        info =  self.nusc.get('sample', self.sample['token'])
        info_2 = self.nusc.get('sample_data',info['data']['LIDAR_TOP'])
        self.file = info_2['filename']

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
                    # cell(x,y).lidar_aantal += 1
                    x,y = None
                number = f.read(4)
            som +=1