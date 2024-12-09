
class Cell:

    priority_layers = ['ped_crossing', 'walkway', 'stop_line', 'lane', 'road_block', 'road_segment', 'drivable_area', 'carpark_area']
    
    severity_scores = {
        'ped_crossing': 10,
        'walkway': 9,
        'stop_line': 8,
        'lane': 7,
        'road_block': 6,
        'road_segment': 5,
        'drivable_area': 4,
        'carpark_area': 3
    }

    def __init__(self, x, y, scene_length,layers = None):
        if layers is None:
            layers = {}
        self.x = x
        self.y = y
        self.occ = [0] * scene_length
        self.layers = layers
        self.layer = 'empty'
        self.total_risk = [0] * scene_length
        self.static_risk = 0
        self.detect_risk = [0] * scene_length
        self.track_risk = [0] * scene_length
        self.isscanned = False
        self.ofinterest = 0
        self.lidar_aantal = [0] * scene_length

    def assign_layer(self, prnt = False):
        if(prnt):
            print("Layers dictionary items for Cell at x={} \t y={} \n{}".format(self.x, self.y, self.layers.keys()))

        layers = self.layers
        self.layers = {}
        # Iterate through the layers dictionary
        for layer_name, token in layers.items():
            # Check if the token is non-empty
            if token:  # token is non-empty (not an empty string or None)
                self.layers.update({layer_name: token})  
                
        if(prnt):
            print('The new self.layers variable keys are = {}'.format(self.layers.keys()))

        for layer_name in Cell.priority_layers:
            if layer_name in self.layers:
                self.layer = layer_name
                break

        # Calculate the static risk as the sum of severity scores for all layers in self.layers
        self.static_risk = sum(Cell.severity_scores.get(layer, 0) for layer in self.layers)

        if(prnt):
            print('The new self.layer variable = {}'.format(self.layer))

    def CalcRisk(self, weights):
        """
        Calculate the total risk as a weighted sum of static_risk, detect_risk, and track_risk.

        :param weights: Tuple of three weights (w_static, w_detect, w_track)
        :return: Total calculated risk
        """
        if len(weights) != 3:
            raise ValueError("Weights must be a tuple of length 3 (w_static, w_detect, w_track).")
        
        w_static, w_detect, w_track = weights
        self.risk = w_static * self.static_risk + w_detect * self.detect_risk + w_track * self.track_risk
        return self.risk


    def to_dict(self):
        """
        Convert the Cell object into a dictionary for saving.
        """
        return {
            'x': self.x,
            'y': self.y,
            'occ': self.occ,
            'total risk': self.total_risk,
            'static risk': self.static_risk,
            'detect risk': self.detect_risk,
            'track risk': self.track_risk,
            'layers': self.layers,
            'layer': self.layer,
            'isscanned': self.isscanned,
            'ofinterest': self.ofinterest,
            'lidar_aantal': self.lidar_aantal
        }

    @staticmethod
    def from_dict(cell_dict, scene_length):
        """
        Convert a dictionary back into a Cell object.

            'total risk': self.total_risk,
            'static risk': self.static_risk,
            'detect risk': self.detect_risk,
            'track risk': self.track_risk,
        """
        cell = Cell(
            x=cell_dict['x'],
            y=cell_dict['y'],
            scene_length=scene_length,
            layers=cell_dict['layers']
        )
        cell.occ = cell_dict['occ']
        cell.total_risk = cell_dict['total risk']
        cell.static_risk = cell_dict['static risk']
        cell.detect_risk = cell_dict['detect risk']
        cell.track_risk = cell_dict['track risk']
        cell.layer = cell_dict['layer']
        cell.isscanned = cell_dict['isscanned']
        cell.ofinterest = cell_dict['ofinterest']
        cell.lidar_aantal = cell_dict['lidar_aantal']
        return cell





