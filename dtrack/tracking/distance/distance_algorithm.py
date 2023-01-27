from abc import ABC, abstractmethod
from typing import Union
from .features import DistanceFeatures
from ..trackable.base_object import TrackableObject
from ...util import Detection


class DistanceAlgorithm(ABC):
    """
    Abstract class for distance algorithms.
    """

    FEATURES_TYPE = DistanceFeatures

    @abstractmethod
    def distance(self, trackable_object: TrackableObject, detection: Detection) -> float:
        """
        Calculates the distance between a trackable object and a detection.

        Args:
            trackable_object (TrackableObject): The trackable object.
            detection (Detection): The detection.

        Returns:
            float: The distance.
        """
        pass
    
    @abstractmethod
    def compute_features(self, target: Union[TrackableObject, Detection]) -> DistanceFeatures:
        """
        Computes the distance features of a trackable object or a detection.

        Args:
            target (Union[TrackableObject, Detection]): The trackable object or the detection.

        Returns:
            DistanceFeatures: The distance features.
        """
        if isinstance(target, TrackableObject):
            return self.FEATURES_TYPE.create_from_trackable_object(target)
        elif isinstance(target, Detection):
            return self.FEATURES_TYPE.create_from_detection(target)
        else:
            raise TypeError(f"Unsupported type: {type(target)}")
