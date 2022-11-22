from typing import List, Union
import cv2
import numpy as np
from .scale_factor import ScaleFactor
from .detection import Detection


class Image:
    """
    Class for images.
    """

    def __init__(self, image: Union[np.ndarray, str]):
        """
        :param image: image
        """
        self._image = image
        self._detections = []

    @property
    def image(self) -> np.ndarray:
        """
        :return: image
        """
        if isinstance(self._image, str):
            self._image = np.array(cv2.imread(self._image))
        return self._image
    
    @property
    def scale_factor(self) -> ScaleFactor:
        """
        :return: scale factor
        """
        return ScaleFactor(*self.image.shape[:2])
    
    @property
    def detections(self) -> List[Detection]:
        """
        :return: detections
        """
        return self._detections

    def __str__(self):
        return f"Image({self.image.shape})"
    
    def __repr__(self):
        return f"Image({self.image.shape})"
    
    def __eq__(self, other):
        return np.array_equal(self.image, other.image)
    
    def __mul__(self, other) -> "Image":
        if isinstance(other, ScaleFactor):
            return Image(cv2.resize(self.image, (int(self.scale_factor.x * other.x), int(self.scale_factor.y * other.y))))
        else:
            raise TypeError(f"Cannot multiply Image by {type(other)}")
    
    def __rmul__(self, other) -> "Image":
        return self * other

    def apply_scale_factor(self, scale_factor: ScaleFactor) -> "Image":
        """
        Apply scale factor to image.
        :param scale_factor: scale factor
        """
        return self * scale_factor
    
    def resize(self, width: int, height: int) -> "Image":
        """
        Resize image.
        :param width: width
        :param height: height
        """
        return Image(cv2.resize(self.image, (width, height)), ScaleFactor(width, height))
    
    def add_detection(self, detection: Detection):
        """
        Add detection to image.
        :param detection: detection
        """
        self._detections.append(detection)
    
    def add_detections(self, detections: List[Detection]):
        """
        Add detections to image.
        :param detections: detections
        """
        self._detections.extend(detections)
