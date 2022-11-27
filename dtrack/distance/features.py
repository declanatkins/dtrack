from abc import ABC, abstractmethod


class DistanceFeatures(ABC):
    """
    Abstract class for distance features.
    """

    @abstractmethod
    def __call__(self, detection1, detection2):
        """
        Calculate the distance features between two detections.

        :param detection1: first detection
        :param detection2: second detection
        :return: distance features between the detections
        """
        raise NotImplementedError("DistanceFeatures is an abstract class.")

    @abstractmethod
    def to_dict(self):
        """
        Convert the distance features to a dictionary.

        :return: dictionary representation of the distance features
        """
        raise NotImplementedError("DistanceFeatures is an abstract class.")
    
    @abstractmethod
    def to_json(self):
        """
        Convert the distance features to a JSON string.

        :return: JSON string representation of the distance features
        """
        raise NotImplementedError("DistanceFeatures is an abstract class.")
    
    @classmethod
    @abstractmethod
    def from_dict(cls, d):
        """
        Create distance features from a dictionary.
        """
        raise NotImplementedError("DistanceFeatures is an abstract class.")

    @classmethod
    @abstractmethod
    def from_json(cls, json):
        """
        Create distance features from a JSON string.
        """
        raise NotImplementedError("DistanceFeatures is an abstract class.")
