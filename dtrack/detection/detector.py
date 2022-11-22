from abc import ABC, abstractmethod
from typing import List


class ObjectDetector(ABC):
    """
    Abstract class for object detectors.
    """

    @abstractmethod
    def detect(self, image: Image) -> List[Detection]:
        """
        Detect objects in the given image.

        :param image: image to detect objects in
        :return: list of detected objects
        """
        raise NotImplementedError("ObjectDetector is an abstract class.")