from nuscenes.nuscenes import NuScenes 
import numpy as np
import os


class Detect:
    def __init__(self, map, dataroot,x,y):
        self._sample=None
        self._x = None
        self._y = None
        self.patchxmin = x
        self.patchymin = y
        self.oud = None
        self.dataroot = dataroot
        self.nusc = NuScenes(version='v1.0-mini', verbose=False)
        self.file = None
        self.map = map

    @property 
    def sample(self): #getter om sample aftelezen
        return self._sample
    
    @sample.setter
    def sample(self, values): #values is een tuple van sample ego_x en ego_y
        self._sample, self._x , self._y = values
        if self._sample != self.oud: # alleen runnen als sample veranderd
            self.file_get()
            self.lidar_coor()
            self.oud = self._sample # sample is helemaal gerund dus dit is de stopconditie
        else: return


    def file_get(self): #Deze functie zoekt het bestand van de lidar pointcloud die bij de sample hoort. Vervolgens wordt het volledige pad er naar toe gemaakt.
        info =  self.nusc.get('sample', self._sample)
        info_2 = self.nusc.get('sample_data',info['data']['LIDAR_TOP'])
        self.file = os.path.join(self.dataroot, info_2['filename'])
        print(type(self.file))

    def lidar_coor(self):#Deze functie Loopt door het bestand heen. Het bestand heeft per Lidar punt een x, y, z coordinaten en de channel index + reflectifity

        som = 0
        lidar_punt=0
        
        with open(self.file, "rb") as f:
            number = f.read(4)
            print (number)
            while number != b"":
                quo, rem = divmod(som,5) #omdat je alleen x en y wilt gebruiken en niet de andere dingen kijk je naar het residu van het item waar die op zit.
                if rem == 0: # als het residu = 0 heb je het x coordinaat en res = 1 is het y-coordinaat
                    x = np.frombuffer(number, dtype=np.float32)
                elif rem ==1:
                    y = np.frombuffer(number, dtype=np.float32)
                    lidar_punt += 1
                    self.map.grid.get_cell(int(x+self._x-595),int(y+self._y-1568)).lidar_aantal +=1
                number = f.read(4) #leest de volgende bit
                print(number)
                print(lidar_punt)
                som +=1 # som houdt bij hoeveel items gelezen zijn.
        print (som)