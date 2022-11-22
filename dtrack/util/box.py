from dataclasses import dataclass
from typing import Tuple
from .scale_factor import ScaleFactor


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
        return self.centre_x - self.width / 2, self.centre_y - self.height / 2
    
    @property
    def top_right(self) -> Tuple[float, float]:
        """
        :return: top right corner of the box
        """
        return self.centre_x + self.width / 2, self.centre_y - self.height / 2

    @property
    def bottom_left(self) -> Tuple[float, float]:
        """
        :return: bottom left corner of the box
        """
        return self.centre_x - self.width / 2, self.centre_y + self.height / 2

    @property
    def bottom_right(self) -> Tuple[float, float]:
        """
        :return: bottom right corner of the box
        """
        return self.centre_x + self.width / 2, self.centre_y + self.height / 2
    
    @property
    def area(self) -> float:
        """
        :return: area of the box
        """
        return self.width * self.height
    
    @property
    def x1(self) -> float:
        """
        :return: x coordinate of the top left corner of the box
        """
        return self.centre_x - self.width / 2
    
    @property
    def x2(self) -> float:
        """
        :return: x coordinate of the top right corner of the box
        """
        return self.centre_x + self.width / 2
    
    @property
    def y1(self) -> float:
        """
        :return: y coordinate of the top left corner of the box
        """
        return self.centre_y - self.height / 2
    
    @property
    def y2(self) -> float:
        """
        :return: y coordinate of the bottom left corner of the box
        """
        return self.centre_y + self.height / 2
    
    def to_coco(self) -> Tuple[float, float, float, float]:
        """
        :return: bounding box in COCO format
        """
        return self.centre_x - self.width / 2, self.centre_y - self.height / 2, self.width, self.height
    
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
    
    def apply_scale_factor(self, scale_factor: ScaleFactor) -> "Box":
        """
        Apply a scale factor to the box.

        :param scale_factor: scale factor to apply
        :return: scaled box
        """
        return self * scale_factor
    
