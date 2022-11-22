from dataclasses import dataclass
from typing import Tuple
from .scale_factor import ScaleFactor
from . import geometry


@dataclass
class Box:
    """
    Bounding box of an object in an image.
    """

    centre_x: float
    centre_y: float
    width: float
    height: float
    angle: float
    scale_factor: ScaleFactor

    @property
    def top_left(self) -> Tuple[float, float]:
        """
        :return: top left corner of the box
        """
        base_point = self.centre_x - self.width / 2, self.centre_y - self.height / 2
        if self.rotated:
           return geometry.rotate_point(*base_point, self.centre_x, self.centre_y, self.angle)
        else:
            return base_point
    
    @property
    def top_right(self) -> Tuple[float, float]:
        """
        :return: top right corner of the box
        """
        base_point = self.centre_x + self.width / 2, self.centre_y - self.height / 2
        if self.rotated:
            return geometry.rotate_point(*base_point, self.centre_x, self.centre_y, self.angle)
        else:
            return base_point

    @property
    def bottom_left(self) -> Tuple[float, float]:
        """
        :return: bottom left corner of the box
        """
        base_point = self.centre_x - self.width / 2, self.centre_y + self.height / 2
        if self.rotated:
            return geometry.rotate_point(*base_point, self.centre_x, self.centre_y, self.angle)
        else:
            return base_point

    @property
    def bottom_right(self) -> Tuple[float, float]:
        """
        :return: bottom right corner of the box
        """
        base_point = self.centre_x + self.width / 2, self.centre_y + self.height / 2
        if self.rotated:
            return geometry.rotate_point(*base_point, self.centre_x, self.centre_y, self.angle)
        else:
            return base_point
    
    @property
    def area(self) -> float:
        """
        :return: area of the box
        """
        return self.width * self.height
    
    @property
    def x1(self) -> float:
        """
        :return: x coordinate of the left of the box
        """
        return self.top_left[0]
    
    @property
    def x2(self) -> float:
        """
        :return: x coordinate of the right of the box
        """
        return self.top_right[0]
    
    @property
    def y1(self) -> float:
        """
        :return: y coordinate of the top of the box
        """
        return self.top_left[1]
    
    @property
    def y2(self) -> float:
        """
        :return: y coordinate of the bottom of the box
        """
        return self.bottom_right[1]
    
    @property
    def rotated(self) -> bool:
        """
        :return: whether the box is rotated
        """
        return self.angle != 0
    
    def to_coco(self) -> Tuple[float, float, float, float]:
        """
        :return: bounding box in COCO format
        """
        return self.x1, self.y1, self.width, self.height
    
    def to_yolo(self) -> Tuple[float, float, float, float]:
        """
        :return: bounding box in YOLO format
        """
        return self.centre_x, self.centre_y, self.width, self.height
    
    def __str__(self):
        return f"Box({self.centre_x}, {self.centre_y}, {self.width}, {self.height}, {self.angle}, {self.scale_factor})"
    
    def __repr__(self):
        return f"Box({self.centre_x}, {self.centre_y}, {self.width}, {self.height}, {self.angle}, {self.scale_factor})"
    
    def __eq__(self, other):
        return self.centre_x == other.centre_x and self.centre_y == other.centre_y and self.width == other.width and self.height == other.height and self.angle == other.angle and self.scale_factor == other.scale_factor
    
    def __mul__(self, other):
        if isinstance(other, ScaleFactor):
            scale_x = other.x / self.scale_factor.x
            scale_y = other.y / self.scale_factor.y
            return Box(self.centre_x * scale_x, self.centre_y * scale_y, self.width * scale_x, self.height * scale_y, self.angle, other)
        else:
            raise TypeError(f"Cannot multiply Box by {type(other)}")
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def apply_scale_factor(self, scale_factor: ScaleFactor) -> "Box":
        """
        Apply a scale factor to the box.

        :param scale_factor: scale factor to apply
        :return: scaled box
        """
        return self * scale_factor

    def rotate(self, angle: float) -> "Box":
        """
        Rotate the box.

        :param angle: angle to rotate by in degrees
        :return: rotated box
        """
        return Box(self.centre_x, self.centre_y, self.width, self.height, self.angle + angle, self.scale_factor)
