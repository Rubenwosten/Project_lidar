from nuscenes import NuScenes
from Object import Object


# this class designates a severity function according to identified objects and their orientation
class severity:
    def factor(traffic_participant, orientation):
        traffic_participant_f = {
        "human.pedestrian.adult": {
            "score": 0.843333333,
            "orientation": 0
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
        orientation_f={
            "front": 1,
            "side": 1,
            "rear": 1
        }

    

        participant_score= traffic_participant_f[traffic_participant]["score"]


        #participant_score=traffic_participant_f.get(traffic_participant, 1)
        io=traffic_participant_f[traffic_participant]["orientation"]
        o_factor= orientation_f.get(orientation, 1)

        print(participant_score, io, o_factor)
        
        if io == 1:
            sev = participant_score * o_factor
            print(sev)
        else:
            sev = participant_score
            print(sev)
        return sev

