
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





