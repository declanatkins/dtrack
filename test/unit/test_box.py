from dtrack.util import Box
from dtrack.util import ScaleFactor

class TestBox:
    """
    Unit tests for the Box class.
    """

    def test_top_left(self):
        """
        Test the top_left property.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        assert box.top_left == (0, 0)
    
    def test_top_left_with_rotation(self):
        """
        Test the top_left property with rotation.
        """
        box = Box(5, 5, 10, 10, 90, ScaleFactor(10, 10))
        assert box.top_left == (10, 0)

    def test_top_right(self):
        """
        Test the top_right property.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        assert box.top_right == (10, 0)
    
    def test_top_right_with_rotation(self):
        """
        Test the top_right property with rotation.
        """
        box = Box(5, 5, 10, 10, 90, ScaleFactor(10, 10))
        assert box.top_right == (10, 10)
    
    def test_bottom_left(self):
        """
        Test the bottom_left property.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        assert box.bottom_left == (0, 10)
    
    def test_bottom_left_with_rotation(self):
        """
        Test the bottom_left property with rotation.
        """
        box = Box(5, 5, 10, 10, 90, ScaleFactor(10, 10))
        assert box.bottom_left == (0, 0)
    
    def test_bottom_right(self):
        """
        Test the bottom_right property.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        assert box.bottom_right == (10, 10)
    
    def test_bottom_right_with_rotation(self):
        """
        Test the bottom_right property with rotation.
        """
        box = Box(5, 5, 10, 10, 90, ScaleFactor(10, 10))
        assert box.bottom_right == (0, 10)

    def test_area(self):
        """
        Test the area property.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        assert box.area == 100
    
    def test_x1(self):
        """
        Test the x1 property.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        assert box.x1 == 0
    
    def test_x2(self):
        """
        Test the x2 property.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        assert box.x2 == 10
    
    def test_y1(self):
        """
        Test the y1 property.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        assert box.y1 == 0
    
    def test_y2(self):
        """
        Test the y2 property.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        assert box.y2 == 10
    
    def test_str(self):
        """
        Test the __str__ method.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        assert str(box) == "Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))"
    
    def test_repr(self):
        """
        Test the __repr__ method.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        assert repr(box) == "Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))"
    
    def test_to_coco(self):
        """
        Test the to_coco method.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        assert box.to_coco() == (0, 0, 10, 10)
    
    def test_apply_scale_factor(self):
        """
        Test the apply_scale_factor method.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        new_box = box.apply_scale_factor(ScaleFactor(20, 20))
        assert new_box == Box(10, 10, 20, 20, 0, ScaleFactor(20, 20))
    
    def test_rotate(self):
        """
        Test the rotate method.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        new_box = box.rotate(90)
        assert new_box == Box(5, 5, 10, 10, 90, ScaleFactor(10, 10))
    
    def test_mul(self):
        """
        Test the __mul__ method.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        new_box = box * ScaleFactor(20, 20)
        assert new_box == Box(10, 10, 20, 20, 0, ScaleFactor(20, 20))

    def test_rmul(self):
        """
        Test the __rmul__ method.
        """
        box = Box(5, 5, 10, 10, 0, ScaleFactor(10, 10))
        new_box = ScaleFactor(20, 20) * box
        assert new_box == Box(10, 10, 20, 20, 0, ScaleFactor(20, 20))