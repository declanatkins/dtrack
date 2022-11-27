from abc import ABC, abstractmethod
from ..util import Detection
from .features import DistanceFeatures
from ..trackable.base_object import BaseTrackableObject

class DistanceAlgorithm(ABC):
    """
    Abstract class for distance algorithms.
    """

    FEATURES_TYPE = DistanceFeatures

    @abstractmethod
    def distance(self, detection1: Detection, detection2: Detection) -> float:
        """
        Calculate the distance between two detections.

        :param detection1: first detection
        :param detection2: second detection
        :return: distance between the detections
        """
        raise NotImplementedError("DistanceAlgorithm is an abstract class.")
    
    def compute_features(self, trackable_object: BaseTrackableObject) -> DistanceFeatures:
        """
        Compute the distance features for the given trackable object.

        :param trackable_object: trackable object to compute the distance features for
        :return: distance features for the trackable object
        """
        return self.FEATURES_TYPE(trackable_object)

    def __call__(self, detection1: Detection, detection2: Detection) -> float:
        """
        Call the distance method.

        :param detection1: first detection
        :param detection2: second detection
        :return: distance between the detections
        """
        return self.distance(detection1, detection2)