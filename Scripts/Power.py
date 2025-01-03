import numpy as np
import math
#lidar_parameters:
erx = 0.9 # receiver optics effeciency
etx = 0.9 # emmitter optics effeciency
n = 1 #target reflectivity
D = 25*pow(10,-3) #diameter lens 25 mm
Aovx = 1/np.pi #1 graden in radialen
Aovy = 1/np.pi #1 graden in radialen
phi_amb = 13.27 #W/m^2 gekozen via tabel want test wast delta labda = 50 nm
Nshots = 1
Ro = 0.9 #We kiezen een ADP lidar met een golflengte van 1550 nm
M = 30
F = 7
Bn = 1* 10^6 #Bandwidth 1 MHz
Id = 150*10^-9 # Dark current 150 nA
Rf = 10*10^3 #feed resistance 10 K ohm
vamp = 28*10^-9 # amplifier input voltage noice density 28 nV/sqrt(Hz)
T =293 #20 graden celsius in K
Kb = 1.380649*10^-23 # boltzmann constant
e = 1.602*10^-19 # elementaire lading
P_false = 10^-4 # false trigger mochten klein zetten


class power:
    def __init__(self, map, reso, n, max_range):
        self.map = map
        self.reso = reso
        self.n_cones = n
        self.max_range = max_range
        self.ego = self.map.ego_positions
        self._sampleindex = None
        self._sample = None
        self.oud = None

        
    @property
    def sample(self): #getter om sample aftelezen
        return self._sample
    
    @sample.setter
    def sample(self, values):
        self._sample, self._sampleindex = values
        cones = self.assign_cell_to_cone()
        for cone in enumerate(cones):
            for cell in cone:
                break




    def cones (self):
        angle_step = 360 / self.n_cones
        quadrants = [(i * angle_step, (i + 1) * angle_step) for i in range(self.n_cones)]
        return quadrants

    def get_angle_and_distance(self, cell):
        ego_pos = self.ego[self._sampleindex]
        x,y = cell
        angle = math.degrees(math.atan2((y-ego_pos[1]),(x-ego_pos[0])))
        distance = math.sqrt((y-ego_pos[1])**2 + (x-ego_pos[0])**2)
        return angle, distance
    
    def assign_cell_to_cone(self):
        cones = self.cones()
        cone_cells = {i: [] for i in range(self.n_cones)}
        for row in map.grid.grid:
            for cell in row:
                angle, distance = self.get_angle_and_distance(cell)

                if distance <= self.max_range:
                    for i, (start_angle, end_angle) in enumerate(cones):
                        if start_angle <= angle < end_angle:
                            cone_cells[i].append((cell, distance))
                            break

        return cone_cells


    def calc_proba(self, power,coor):
        r = np.sqrt((coor[0]-self.ego[self._sampleindex][0])^2+(coor[1]-self.ego[self._sampleindex][1])^2)
        amp_area = np.pi*(D/2)^2
        P_s = (1/(2*np.pi*r^2))*power*erx*etx*n*amp_area
        Aov = 4*r^2*np.tan(Aovx/2)*np.tan(Aovy/2)
        P_b = (1/(2*np.pi*r^2))*phi_amb*amp_area*Aov*erx*n
        SNR = np.sqrt(Nshots*Ro^2*P_s^2)/np.sqrt(2*e*Bn*F*(Ro*(P_s+P_b)+Id)+(Bn/M^2)*(4*Kb*T/Rf + (vamp/Rf)^2))
        Prob = 0.5*math.erfc(np.sqrt(-math.log(P_false))-np.sqrt(SNR+0.5))
        return Prob

