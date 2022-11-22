class ScaleFactor:
    """
    Scale factor for a detection, image or bounding box.
    """

    def __init__(self, x: float, y: float):
        """
        :param x: scale factor in x direction
        :param y: scale factor in y direction
        """
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"ScaleFactor({self.x}, {self.y})"
    
    def __repr__(self):
        return f"ScaleFactor({self.x}, {self.y})"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    