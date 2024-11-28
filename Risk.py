# This class handles the risk function(s)
class Risk:

    _instance = None  # Class-level attribute to store the singleton instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            # Create the instance if it doesn't exist
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Initialize only if this is the first time the instance is created
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self.initialized = True


    def CalcRisk(self):
        self.StaticRisk(self)
        self.DetectionRisk(self)
        self.TrackingRisk(self)
        return

    def StaticRisk(self):
        return

    def DetectionRisk(self):
        return

    def TrackingRisk(self):
        return




