import json

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

    @classmethod
    def from_json(cls, json_string):
        """
        :param json_string: JSON representation of a scale factor
        :return: scale factor
        """
        return cls(**json.loads(json_string))
    
    @classmethod
    def from_dict(cls, d):
        """
        :param d: dictionary representation of a scale factor
        :return: scale factor
        """
        return cls(**d)

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __str__(self):
        return f"ScaleFactor({self.x}, {self.y})"
    
    def __repr__(self):
        return f"ScaleFactor({self.x}, {self.y})"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def to_json(self):
        """
        :return: JSON representation of the scale factor
        """
        return json.dumps(self.__dict__())
    
    def to_dict(self):
        """
        :return: dictionary representation of the scale factor
        """
        return {
            'x': self.x,
            'y': self.y
        }