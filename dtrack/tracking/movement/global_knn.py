import json
from typing import List, Tuple
import numpy as np
from .base_predictor import BaseMovementPredictor
from ...util.singleton import Singleton


class GlobalKNNPredictor(BaseMovementPredictor, Singleton):
    """
    Global KNN movement predictor. This class is a Singleton.
    """

    def __init__(self, k=3, max_history=5000):
        self.k = k
        self.dataset = []
        self.max_history = max_history

    def _convert_to_prediction_feature(self, x: int, y: int, location_history: List[Tuple[int, int]]) -> List[float]:
        """
        Convert the inputted data to a feature vector to use for prediction.

        The feature vector is defined as follows:
        [
            x, - The current x coordinate
            y, - The current y coordinate
            incoming_x_velocity, - delta x at the last coordinate
            incoming_y_velocity, - delta y at the last coordinate
            incoming_x_acceleration, - dy/dx at the last x coordinate
            incoming_y_acceleration - dy/dx at the last y coordinate
        ]
        """
        n_locations = len(location_history)
        if n_locations:
            last_x, last_y = location_history[-1]
            incoming_x_velocity = x - last_x
            incoming_y_velocity = y - last_y
        else:
            incoming_x_velocity = 0
            incoming_y_velocity = 0
        if n_locations > 1:
            second_last_x, second_last_y = location_history[-2]
            previous_x_velocity = last_x - second_last_x
            previous_y_velocity = last_y - second_last_y
            incoming_x_acceleration = incoming_x_velocity - previous_x_velocity
            incoming_y_acceleration = incoming_y_velocity - previous_y_velocity
        else:
            incoming_x_acceleration = 0
            incoming_y_acceleration = 0 
        return [x, y, incoming_x_velocity, incoming_y_velocity, incoming_x_acceleration, incoming_y_acceleration]
    
    def _convert_to_training_feature(location_history: List[Tuple[int, int]]) -> List[float]:
        """
        Convert the last location history value to a feature vector to use for training.

        The feature vector is defined as follows:
        [
            x, - The current x coordinate
            y, - The current y coordinate
            incoming_x_velocity, - delta x at the last coordinate
            incoming_y_velocity, - delta y at the last coordinate
            incoming_x_acceleration, - dy/dx at the last x coordinate
            incoming_y_acceleration - dy/dx at the last y coordinate
            outgoing_x_velocity, - delta x at the next coordinate, ie what to predict
            outgoing_y_velocity, - delta y at the next coordinate, ie what to predict
        ]
        """
        if len(location_history) < 4:
            return None
        
        x, y = location_history[-1]
        prev_x, prev_y = location_history[-2]
        prev_prev_x, prev_prev_y = location_history[-3]
        prev_prev_prev_x, prev_prev_prev_y = location_history[-4]

        outgoing_x_velocity = x - prev_x
        outgoing_y_velocity = y - prev_y
        incoming_x_velocity = prev_x - prev_prev_x
        incoming_y_velocity = prev_y - prev_prev_y
        incoming_x_acceleration = incoming_x_velocity - (prev_prev_x - prev_prev_prev_x)
        incoming_y_acceleration = incoming_y_velocity - (prev_prev_y - prev_prev_prev_y)

        return [
            prev_x,
            prev_y,
            incoming_x_velocity,
            incoming_y_velocity,
            incoming_x_acceleration,
            incoming_y_acceleration,
            outgoing_x_velocity,
            outgoing_y_velocity
        ]

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
        if len(self.dataset) < self.k:
            return x, y
        if len(location_history) >= 4:
            self.dataset.append(self._convert_to_training_feature(location_history))
            if len(self.dataset) > self.max_history:
                self.dataset = self.dataset[1:]

        feature = self._convert_to_prediction_feature(x, y, location_history)
        distances = []
        for data in self.dataset:
            distances.append((np.linalg.norm(np.array(data[:-2]) - np.array(feature)), data[-2], data[-1]))
        distances.sort(key=lambda x: x[0])
        distances = distances[:self.k]
        x_velocity = sum([x[1] for x in distances]) / self.k
        y_velocity = sum([x[2] for x in distances]) / self.k
        return x + x_velocity, y + y_velocity
    
    def predict_locations(self, x: float, y: float, location_history: List[Tuple[float, float]], n: int) -> List[Tuple[float, float]]:
        """
        Predict the next n locations of the object.

        :param x: current x coordinate
        :param y: current y coordinate
        :param location_history: location history
        :param n: number of locations to predict
        :return: predicted locations
        """
        locations = []
        mutable_location_history = location_history.copy()
        backup_dataset = self.dataset.copy()
        for _ in range(n):
            x, y = self.predict(x, y, mutable_location_history)
            locations.append((x, y))
            mutable_location_history.append((x, y))
        self.dataset = backup_dataset
        return locations
    
    def to_dict(self):
        return {
            "k": self.k,
            "max_history": self.max_history,
            "dataset": self.dataset
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: dict):
        object = cls(data["k"], data["max_history"])
        object.dataset = data["dataset"]
        return object
    
    @classmethod
    def from_json(cls, data: str):
        return cls.from_dict(json.loads(data))
    
    def __str__(self):
        return f"KNNPredictor(k={self.k}, max_history={self.max_history})"
    
    def __repr__(self):
        return self.__str__()
