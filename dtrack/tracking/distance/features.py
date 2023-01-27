from abc import ABC, abstractmethod
from ..trackable.base_object import TrackableObject
from ...util import Detection


class DistanceFeatures(ABC):
    """
    Abstract class for distance features.
    """
    @abstractmethod
    @classmethod
    def from_json(cls, json_object: dict) -> 'DistanceFeatures':
        """
        Creates a new distance features object from a JSON object.

        Args:
            json_object (dict): The JSON object.

        Returns:
            DistanceFeatures: The distance features object.
        """
        pass

    @abstractmethod
    @classmethod
    def create_from_detection(cls, detection: Detection) -> 'DistanceFeatures':
        """
        Creates a new distance features object from a detection.

        Args:
            detection (Detection): The detection.

        Returns:
            DistanceFeatures: The distance features object.
        """
        pass
    
    @abstractmethod
    @classmethod
    def create_from_trackable_object(cls, trackable_object: TrackableObject) -> 'DistanceFeatures':
        """
        Creates a new distance features object from a trackable object.

        Args:
            trackable_object (TrackableObject): The trackable object.

        Returns:
            DistanceFeatures: The distance features object.
        """
        pass

    
    @abstractmethod
    def to_json(self) -> dict:
        """
        Converts the distance features to a JSON object.

        Returns:
            dict: The JSON object.
        """
        pass
