from abc import ABC, abstractmethod
from collections import Counter
from typing import List, Tuple
import numpy as np
from ...util import Box, Detection
from ..movement.predictor import MovementPredictor
from ..distance.features import DistanceFeatures


class TrackableObject(ABC):
    """
    Abstract class for trackable objects.
    """

    def __init__(
            self,
            class_name: str,
            subclass_name: str,
            bounding_box: Box,
            movement_predictor: MovementPredictor,
            first_seen: int,
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
        self._class_name = class_name
        self._subclass_name = [subclass_name]
        self._bounding_box = bounding_box
        self._mask = mask
        self._features = features
        self._location_history = [(bounding_box.cx, bounding_box.cy)]
        self._tracking_attributes = tracking_attributes
        self._movement_predictor = movement_predictor
        self._first_seen = first_seen
        self._last_seen = first_seen
    
    @property
    def class_name(self) -> str:
        """
        :return: class name
        """
        return self._class_name
    
    @property
    def subclass_name(self) -> str:
        """
        :return: subclass name
        """
        return Counter(self._subclass_name).most_common(1)[0][0]
    
    @property
    def bounding_box(self) -> Box:
        """
        :return: bounding box
        """
        return self._bounding_box
    
    @property
    def mask(self) -> np.ndarray:
        """
        :return: mask
        """
        return self._mask
    
    @property
    def features(self) -> DistanceFeatures:
        """
        :return: distance features
        """
        return self._features
    
    @features.setter
    def features(self, features: DistanceFeatures):
        """
        Set the distance features.

        :param features: distance features
        """
        self._features = features
    
    @property
    def location_history(self) -> list:
        """
        :return: location history
        """
        return self._location_history
    
    @property
    def location(self) -> tuple:
        """
        :return: current location
        """
        return self._location_history[-1]
    
    @property
    def first_seen(self) -> int:
        """
        :return: first seen
        """
        return self._first_seen
    
    @property
    def last_seen(self) -> int:
        """
        :return: last seen
        """
        return self._last_seen

    @classmethod
    @abstractmethod
    def from_detection(cls, detection: Detection, movement_predictor: MovementPredictor, first_seen: int):
        """
        Create a trackable object from a detection.

        :param detection: detection
        :param movement_predictor: movement predictor
        :return: trackable object
        """
        raise NotImplementedError("BaseTrackableObject is an abstract class.")
    
    @classmethod
    @abstractmethod
    def from_json(cls, json_string):
        """
        Create a trackable object from a JSON string.

        :param json_string: JSON string
        :return: trackable object
        """
        raise NotImplementedError("BaseTrackableObject is an abstract class.")
    
    @classmethod
    @abstractmethod
    def from_dict(cls, d):
        """
        Create a trackable object from a dictionary.

        :param d: dictionary
        :return: trackable object
        """
        raise NotImplementedError("BaseTrackableObject is an abstract class.")

    @abstractmethod
    def to_json(self):
        """
        Convert the trackable object to a JSON string.

        :return: JSON string representation of the trackable object
        """
        raise NotImplementedError("BaseTrackableObject is an abstract class.")
    
    @abstractmethod
    def to_dict(self):
        """
        Convert the trackable object to a dictionary.

        :return: dictionary representation of the trackable object
        """
        raise NotImplementedError("BaseTrackableObject is an abstract class.")
    
    @abstractmethod
    def update(self, detection: Detection, frame_number: int):
        """
        Update the trackable object with a new detection.

        :param detection: detection
        """
        raise NotImplementedError("BaseTrackableObject is an abstract class.")

    def predict_locations(self, n: int) -> List[Tuple[float, float]]:
        """
        Predict the next n locations of the trackable object.

        :param n: number of locations to predict
        :return: predicted locations
        """
        return self._movement_predictor.predict_locations(
            *self._location_history[-1],
            self._location_history[:-1],
            n
        )
    
    def get_tracking_attribute(self, attribute_name: str):
        """
        Get a tracking attribute.

        :param attribute_name: attribute name
        :return: attribute value
        """
        try:
            return self._tracking_attributes[attribute_name]
        except KeyError:
            raise AttributeError(f"Attribute '{attribute_name}' not found.")
        
    def set_tracking_attribute(self, attribute_name: str, attribute_value):
        """
        Set a tracking attribute.

        :param attribute_name: attribute name
        :param attribute_value: attribute value
        """
        if not attribute_name in self._tracking_attributes:
            raise AttributeError(f"Attribute '{attribute_name}' not found.")
        self._tracking_attributes[attribute_name] = attribute_value