from typing import Union
import cv2
import numpy as np
from .scale_factor import ScaleFactor


class Image:
    """
    Class for images.
    """

    def __init__(self, image: Union[np.ndarray, str]):
        """
        :param image: image
        """
        self.__image = image

    @property
    def image(self) -> np.ndarray:
        """
        :return: image
        """
        if isinstance(self.__image, str):
            self.__image = np.array(cv2.imread(self.__image))
        return self.__image
    
    @property
    def scale_factor(self) -> ScaleFactor:
        """
        :return: scale factor
        """
        return ScaleFactor(*self.image.shape[:2])

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
    
    def apply_scale_factor(self, scale_factor: ScaleFactor) -> "Image":
        """
        Apply scale factor to image.

        :param scale_factor: scale factor
        """
        return self * scale_factor
    