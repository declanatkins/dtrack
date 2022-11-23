import numpy as np
from dtrack.util.image import Image
from dtrack.util.scale_factor import ScaleFactor
from dtrack.util.detection import Detection
from dtrack.util.box import Box
from tests.assertions import assert_ignore_whitespace_string_equal

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
        assert image._image_content is None
        image.image
        assert isinstance(image._image_content, np.ndarray)
    
    def test_add_detections(self):
        """
        Test the add_detections method.
        """
        image = Image("tests/data/test.jpg")
        assert image.detections == []

        image.add_detections([Detection("test", 0.5, Box(0, 0, 10, 10, 0, ScaleFactor(100, 100)), None)])
        assert image.detections == [Detection("test", 0.5, Box(0, 0, 10, 10, 0, ScaleFactor(100, 100)), None)]
    
    def test_str(self):
        """
        Test the __str__ method.
        """
        image = Image("tests/data/test.jpg")
        assert_ignore_whitespace_string_equal(str(image), "Image(filename=tests/data/test.jpg shape=(100, 100) detections=[])")