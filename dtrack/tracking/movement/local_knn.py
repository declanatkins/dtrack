from typing import List, Tuple
import json
import numpy as np
from .predictor import MovementPredictor


class LocalKNNPredictor(MovementPredictor):
    """
    Local KNN movement predictor.
    """

    def __init__(self, k=3, max_history=5000):
        self.k = k
        self.max_history = max_history

    def predict(self, x: float, y: float, location_history: List[Tuple[float, float]]) -> Tuple[float, float]:
        """
        Predict the next location of the object.

        :param x: current x coordinate
        :param y: current y coordinate
        :param location_history: location history
        :return: predicted location
        """
        if len(location_history) < 2:
            return x, y

        location_history = np.array(location_history)
        last_2_locations = location_history[-2:]
        velocity = last_2_locations[1] - last_2_locations[0]
        predicted_location = last_2_locations[1] + velocity
        return tuple(predicted_location)

    def predict_locations(self, x: float, y: float, location_history: List[Tuple[float, float]], n: int) -> List[Tuple[float, float]]:
        """
        Predict the next n locations of the object.

        :param x: current x coordinate
        :param y: current y coordinate
        :param location_history: location history
        :param n: number of locations to predict
        :return: predicted locations
        """
        predicted_locations = []
        mutable_history = location_history.copy()
        for _ in range(n):
            x, y = self.predict(x, y, mutable_history)
            predicted_locations.append((x, y))
            mutable_history.append((x, y))
        return predicted_locations

    def to_json(self):
        """
        Convert the movement predictor to a JSON string.

        :return: JSON string representation of the movement predictor
        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """
        Convert the movement predictor to a dictionary.

        :return: dictionary representation of the movement predictor
        """
        return {
            'k': self.k,
            'max_history': self.max_history,
            'dataset': self.dataset
        }

    def __str__(self):
        return 'LocalKNNPredictor(k={}, max_history={})'.format(self.k, self.max_history)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_json(cls, json_string: str):
        """
        Create a movement predictor from a JSON string.

        :param json_string: JSON string
        :return: movement predictor
        """
        return cls.from_dict(json.loads(json_string))
    
    @classmethod
    def from_dict(cls, dictionary: dict):
        """
        Create a movement predictor from a dictionary.

        :param dictionary: dictionary
        :return: movement predictor
        """
        object = cls(dictionary['k'], dictionary['max_history'])
        object.dataset = dictionary['dataset']
        return object