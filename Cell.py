
class Cell:

    priority_layers = ['ped_crossing', 'walkway', 'stop_line', 'lane', 'road_block', 'road_segment', 'drivable_area', 'carpark_area']
    

    def __init__(self, x, y, occ = 1, risk = 0, layers = None):
        if layers is None:
            layers = {}
        self.x = x
        self.y = y
        self.occ = occ
        self.layers = layers
        self.layer = 'empty'
        self.risk = risk 
        self.isscanned = False
        self.ofinterest = 0

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

        if(prnt):
            print('The new self.layer variable = {}'.format(self.layer))

    def to_dict(self):
        """
        Convert the Cell object into a dictionary for saving.
        """
        return {
            'x': self.x,
            'y': self.y,
            'occ': self.occ,
            'risk': self.risk,
            'layers': self.layers,
            'layer': self.layer,
            'isscanned': self.isscanned,
            'ofinterest': self.ofinterest
        }

    @staticmethod
    def from_dict(cell_dict):
        """
        Convert a dictionary back into a Cell object.
        """
        cell = Cell(
            x=cell_dict['x'],
            y=cell_dict['y'],
            occ=cell_dict['occ'],
            risk=cell_dict['risk'],
            layers=cell_dict['layers']
        )
        cell.layer = cell_dict['layer']
        cell.isscanned = cell_dict['isscanned']
        cell.ofinterest = cell_dict['ofinterest']
        return cell





