import numpy as np
from nuscenes import NuScenes



# this class designates a severity function according to identified objects and their orientation
class severity:

    def orientation_assign(angle):
        if 315<= angle or angle < 45 :
            return "front"
        elif 45 <= angle < 135: 
            return "side"
        elif 135 <= angle < 225:
            return "rear"
        elif 225 <= angle <315:
            return "side"


    def factor(traffic_participant, participant_facing, participant_position, ego_facing, self_x, self_y): 
        traffic_participant_f = {       #the dictionary which defines severity factor according to traffic participant
        "human.pedestrian.adult": {
            "score": 0.843333333,       #the factor based on category
            "orientation": 0            #wether the orientation of the participant is relevant or not
        },
        "human.pedestrian.child": {
            "score": 0.873,
            "orientation": 0
        },
        "human.pedestrian.constructi": {
            "score": 0.902666667,
            "orientation": 0
        },
        "human.pedestrian.personal_m": {
            "score": 0.932333333,
            "orientation": 0
        },
        "human.pedestrian.police_off": {
            "score": 0.962,
            "orientation": 0
        },
        "movable_object.barrier": {
            "score": 0.991666667,
            "orientation": 0
        },
        "movable_object.debris": {
            "score": 1.021333333,
            "orientation": 0
        },
        "movable_object.pushable_pul": {
            "score": 1.051,
            "orientation": 0
        },
        "movable_object.trafficcone": {
            "score": 1.080666667,
            "orientation": 0
        },
        "static_object.bicycle_rack": {
            "score": 1.110333333,
            "orientation": 0
        },
        "vehicle.bicycle": {
            "score": 1.14,
            "orientation": 1
        },
        "vehicle.bus.bendy": {
            "score": 1.169666667,
            "orientation": 1
        },
        "vehicle.bus.rigid": {
            "score": 1.199333333,
            "orientation": 1
        },
        "vehicle.car": {
            "score": 1.229,
            "orientation": 1
        },
        "vehicle.construction": {
            "score": 1.258666667,
            "orientation": 1
        },
        "vehicle.motorcycle": {
            "score": 1.288333333,
            "orientation": 1
        },
        "vehicle.trailer": {
            "score": 1.318,
            "orientation": 1
        },
        "vehicle.truck": {
            "score": 1.347666667,
            "orientation": 1
        }



        }
        orientation_f={             #the dictionary defining the orientation factor vs ego vehicle
            "front": 1.5,
            "side": 1,
            "rear": 0.9
        }

        ego_orientation_f={         # the orientation factor of the ego vegicle
            "front": 2,
            "side": 1.5,
            "rear": 1
        }
    

        #evaluating the orientations of both vehicles
        participant_x, participant_y = participant_position
        v_e_p= np.array([participant_x - self_x, participant_y - self_y])
        uv= v_e_p / np.linalg.norm (v_e_p)


        ego_angle = np.arccos(np.dot(ego_facing, uv))
        ego_orientation= severity.orientation_assign(ego_angle)

        participant_angle = np.arccos(np.dot(participant_facing, -uv))
        orientation = severity.orientation_assign(participant_angle)
            
        
        
        



        #extracting all values according to the traffic participant
        participant_score= traffic_participant_f[traffic_participant]["score"]
        io=traffic_participant_f[traffic_participant]["orientation"]
        o_factor= orientation_f.get(orientation, 1)
        e_o_factor= ego_orientation_f.get(ego_orientation, 1)

        #debug
        print(participant_score, io, o_factor, e_o_factor)
        
        #severity calculation function
        if io == 1:
            sev = participant_score * o_factor * e_o_factor
            print(sev)
        else:
            sev = participant_score * e_o_factor
            print(sev)
        return sev


