import json
import numpy as np
from ...util.box import Box
from ...util.detection import Detection
from ..movement.base_predictor import BaseMovementPredictor
from ..distance.features import DistanceFeatures
from .base_object import TrackableObject


class DefaultTrackableObject(TrackableObject):
    """
    Default trackable object.
    """

    def __init__(
            self,
            class_name: str,
            subclass_name: str,
            bounding_box: Box,
            movement_predictor: BaseMovementPredictor,
            mask: np.ndarray = None,
            features: DistanceFeatures = None,
            **tracking_attributes
    ):
        """
        Initialize the trackable object.

        :param class_name: class
        :param subclass_name: subclass
        :param bounding_box: bounding box of the object
        :param mask: mask of the object
        :param features: distance features of the object
        :param tracking_attributes: additional tracking attributes
        """
        super().__init__(
            class_name,
            subclass_name,
            bounding_box,
            movement_predictor,
            mask,
            features,
            **tracking_attributes
        )
    
    def to_json(self):
        """
        Convert the trackable object to a JSON string.

        :return: JSON string representation of the trackable object
        """
        return json.dumps(self.to_dict())
    
    def to_dict(self):
        return {
            "class_name": self.class_name,
            "subclass_name": self.subclass_name,
            "bounding_box": self.bounding_box.to_dict(),
            "mask": self.mask.tolist() if self.mask is not None else None,
            "features": self.features.to_dict() if self.features is not None else None,
            "tracking_attributes": self.tracking_attributes,
            "location_history": self.location_history,
            "movement_predictor": self.movement_predictor.to_dict()
        }
    
    @classmethod
    def from_json(cls, json_string: str):
        """
        Create a trackable object from a JSON string.

        :param json_string: JSON string representation of the trackable object
        :return: trackable object
        """
        return cls.from_dict(json.loads(json_string))
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a trackable object from a dictionary.

        :param data: dictionary representation of the trackable object
        :return: trackable object
        """
        return cls(
            data["class_name"],
            data["subclass_name"],
            Box.from_dict(data["bounding_box"]),
            BaseMovementPredictor.from_dict(data["movement_predictor"]),
            np.array(data["mask"]) if data["mask"] is not None else None,
            DistanceFeatures.from_dict(data["features"]) if data["features"] is not None else None,
            **data["tracking_attributes"]
        )
    
    @classmethod
    def from_detection(cls, detection: Detection, movement_predictor: BaseMovementPredictor):
        """
        Create a trackable object from a detection.

        :param detection: detection
        :param movement_predictor: movement predictor
        :return: trackable object
        """
        return cls(
            detection.class_name,
            detection.subclass_name,
            detection.bounding_box,
            movement_predictor,
            detection.mask,
            detection.features,
            **detection.tracking_attributes
        )
    
    def update(self, detection: Detection):
        """
        Update the trackable object with a new detection.
        """
        self._bounding_box = detection.bounding_box
        self._mask = detection.mask
        self._features = detection.features
        self._location_history.append((detection.bounding_box.cx, detection.bounding_box.cy))
        self._tracking_attributes = detection.tracking_attributes
        self._subclass_name.append(detection.subclass_name)

    
