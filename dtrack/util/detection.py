from dataclasses import dataclass
import json
import numpy as np
from .box import Box
from .json_encoder import DTrackJsonEncoder
from .scale_factor import ScaleFactor


@dataclass
class Detection:
    """
    Detection of an object in an image.
    """
    label: str
    confidence: float
    box: Box
    mask: np.ndarray

    @classmethod
    def from_json(cls, json_string):
        """
        :param json_string: JSON representation of a detection
        :return: detection
        """
        dict_object = json.loads(json_string)
        return cls.from_dict(dict_object)
    
    @classmethod
    def from_dict(cls, d):
        """
        :param d: dictionary representation of a detection
        :return: detection
        """
        if not isinstance(d['box'], Box):
            d['box'] = Box.from_dict(d['box'])
        return cls(**d)

    def __hash__(self):
        return hash((self.label, self.confidence, self.box, self.mask))

    def __str__(self):
        return f"Detection(box={self.box}, label={self.label}, confidence={self.confidence})"
    
    def __repr__(self):
        return f"Detection(box={self.box}, label={self.label}, confidence={self.confidence})"
    
    def __eq__(self, other):
        return self.label == other.label and self.confidence == other.confidence and self.box == other.box
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def to_json(self):
        """
        :return: JSON representation of the detection
        """
        return json.dumps(dict(self), cls=DTrackJsonEncoder)
    
    def to_dict(self):
        """
        :return: dictionary representation of the detection
        """
        return {
            'label': self.label,
            'confidence': self.confidence,
            'box': self.box.to_dict(),
            'mask': self.mask
        }

    def scaled(self, scale_factor: ScaleFactor) -> "Detection":
        """
        :param scale_factor: scale factor to apply
        :return: scaled detection
        """
        return Detection(self.label, self.confidence, self.box * scale_factor, self.mask)
