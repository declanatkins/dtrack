import numpy as np
from dtrack.util.image import Image
from dtrack.util.scale_factor import ScaleFactor
from dtrack.util.detection import Detection
from dtrack.util.box import Box

class TestImage:

    def test_image(self):
        """
        Test the image property.
        """
        image = Image("tests/data/test.jpg")
        np.testing.assert_array_equal(image.image, np.zeros((100, 100, 3), dtype=np.uint8))
    
    def test_scale_factor(self):
        """
        Test the scale_factor property.
        """
        image = Image("tests/data/test.jpg")
        assert image.scale_factor == ScaleFactor(100, 100)

    def test_detections(self):
        """
        Test the detections property.
        """
        image = Image("tests/data/test.jpg")
        assert image.detections == []

        image.add_detection(Detection("test", 0.5, Box(0, 0, 10, 10, 0, ScaleFactor(100, 100)), None))
        assert image.detections == [Detection("test", 0.5, Box(0, 0, 10, 10, 0, ScaleFactor(100, 100)), None)]
    
    def test_add_detection(self):
        """
        Test the add_detection method.
        """
        image = Image("tests/data/test.jpg")
        assert image.detections == []

        image.add_detection(Detection("test", 0.5, Box(0, 0, 10, 10, 0, ScaleFactor(100, 100)), None))
        assert image.detections == [Detection("test", 0.5, Box(0, 0, 10, 10, 0, ScaleFactor(100, 100)), None)]
    
    def test_lazy_image_load_funtionality(self):
        """
        Test the lazy image load functionality.
        """
        image = Image("tests/data/test.jpg")
        assert isinstance(image._image, str)
        image.image
        assert isinstance(image._image, np.ndarray)