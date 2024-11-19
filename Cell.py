
class Cell:

    def __init__(self, x, y, occ = 1, layer = '', risk = 0):
        self.x = x
        self.y = y
        self.occ = occ
        self.layer = layer
        self.risk = risk 
        self.isscanned = False
        self.ofinterest = 0
