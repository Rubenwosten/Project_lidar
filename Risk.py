# This class handles the risk function(s)
class Risk:

    _instance = None  # Class-level attribute to store the singleton instance

    weights = (1, 1, 1)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            # Create the instance if it doesn't exist
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Initialize only if this is the first time the instance is created
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self.initialized = True

    
    def CalcRisk(self, map, weights):
        for cell in map.grid:
            cell.detect_risk = self.DetectionRisk(cell)
            cell.track_risk = self.self.TrackingRisk(cell)
            cell.CalcRisk(weights)
        return
    

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

    # Is handled in the layer assignment code
    def StaticRisk(self):
        return

    def DetectionRisk(self):
        return

    def TrackingRisk(self):
        return




