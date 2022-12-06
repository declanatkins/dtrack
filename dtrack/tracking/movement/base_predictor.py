from abc import ABC, abstractmethod
from typing import List, Tuple


class BaseMovementPredictor(ABC):
    """
    Abstract class for movement predictors.
    """

    def predict(self, x: float, y: float, location_history: List[Tuple[float, float]]) -> Tuple[float, float]:
        """
        Predict the next location of the object.

        :param x: current x coordinate
        :param y: current y coordinate
        :param location_history: location history
        :return: predicted location
        """
        pass
    
    def predict_locations(self, x: float, y: float, location_history: List[Tuple[float, float]], n: int) -> List[Tuple[float, float]]:
        """
        Predict the next n locations of the object.

        :param x: current x coordinate
        :param y: current y coordinate
        :param location_history: location history
        :param n: number of locations to predict
        :return: predicted locations
        """
        pass
    
    def __str__(self):
        return self.__class__.__name__
    
    def __repr__(self):
        return self.__str__()
    
    @abstractmethod
    def to_json(self):
        """
        Convert the movement predictor to a JSON string.

        :return: JSON string representation of the movement predictor
        """
        raise NotImplementedError("BaseMovementPredictor is an abstract class.")
    
    @abstractmethod
    def to_dict(self):
        """
        Convert the movement predictor to a dictionary.

        :return: dictionary representation of the movement predictor
        """
        raise NotImplementedError("BaseMovementPredictor is an abstract class.")
    
    @classmethod
    @abstractmethod
    def from_json(cls, json_string):
        """
        Create a movement predictor from a JSON string.

        :param json_string: JSON string
        :return: movement predictor
        """
        raise NotImplementedError("BaseMovementPredictor is an abstract class.")
    
    @classmethod
    @abstractmethod
    def from_dict(cls, d):
        """
        Create a movement predictor from a dictionary.

        :param d: dictionary
        :return: movement predictor
        """
        raise NotImplementedError("BaseMovementPredictor is an abstract class.")
    