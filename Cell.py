
class Cell:

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
            print("Layers dictionary items for Cell at x={} \t y={} \n{}".format(self.x, self.y, self.layers.items()))

        # Iterate through the layers dictionary
        for layer_name, token in self.layers.items():
            # Check if the token is non-empty
            if token:  # token is non-empty (not an empty string or None)
                self.layer = layer_name  # Assign the layer_name to class variable 'layer'
                break  # Exit the loop after assigning the first non-empty layer





