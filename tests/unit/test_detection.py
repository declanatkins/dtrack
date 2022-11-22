from dtrack.util import Box
from dtrack.util import ScaleFactor
from dtrack.util.detection import Detection
from tests.assertions import assert_ignore_whitespace_string_equal


class TestDetection:

    def test_from_json(self):
        """
        Test the from_json method.
        """
        json = """{
            "box": {
                "cx": 0.0,
                "cy": 0.0,
                "width": 10.0,
                "height": 10.0,
                "angle": 0.0,
                "scale_factor": {
                    "x": 1.0,
                    "y": 1.0
                }
            },
            "label": "test",
            "confidence": 0.5,
            "mask": null
        }"""

        detection = Detection.from_json(json)
        assert detection.box.cx == 0.0
        assert detection.box.cy == 0.0
        assert detection.box.width == 10.0
        assert detection.box.height == 10.0
        assert detection.box.angle == 0.0
        assert detection.label == "test"
        assert detection.confidence == 0.5
        assert detection.mask is None
        assert detection.box.scale_factor.x == 1.0
        assert detection.box.scale_factor.y == 1.0
    
    def test_from_dict(self):
        """
        Test the from_dict method.
        """
        d = {
            "box": {
                "cx": 0.0,
                "cy": 0.0,
                "width": 10.0,
                "height": 10.0,
                "angle": 0.0,
                "scale_factor": {
                    "x": 1.0,
                    "y": 1.0
                }
            },
            "label": "test",
            "confidence": 0.5,
            "mask": None
        }

        detection = Detection.from_dict(d)
        assert detection.box.cx == 0.0
        assert detection.box.cy == 0.0
        assert detection.box.width == 10.0
        assert detection.box.height == 10.0
        assert detection.box.angle == 0.0
        assert detection.label == "test"
        assert detection.confidence == 0.5
        assert detection.mask is None
        assert detection.box.scale_factor.x == 1.0
        assert detection.box.scale_factor.y == 1.0
    
    def test__eq__(self):
        """
        Test the __eq__ method.
        """
        d1 = Detection("test", 0.5, Box(0.0, 0.0, 10.0, 10.0, 0.0, ScaleFactor(1.0, 1.0)), None)
        d2 = Detection("test", 0.5, Box(0.0, 0.0, 10.0, 10.0, 0.0, ScaleFactor(1.0, 1.0)), None)
        assert d1 == d2
    
    def test__ne__(self):
        """
        Test the __ne__ method.
        """
        d1 = Detection("test", 0.5, Box(0.0, 0.0, 10.0, 10.0, 0.0, ScaleFactor(1.0, 1.0)), None)
        d2 = Detection("test", 0.5, Box(1.0, 0.0, 10.0, 10.0, 0.0, ScaleFactor(1.0, 1.0)), None)
        assert d1 != d2

    def test__str__(self):
        """
        Test the __str__ method.
        """
        d1 = Detection("test", 0.5, Box(0.0, 0.0, 10.0, 10.0, 0.0, ScaleFactor(1.0, 1.0)), None)
        assert_ignore_whitespace_string_equal(str(d1), "Detection(box=Box(cx=0.0, cy=0.0, width=10.0, height=10.0, angle=0.0, scale_factor=ScaleFactor(x=1.0, y=1.0)), label=test, confidence=0.5, mask=None)")
    
    def test__repr__(self):
        """
        Test the __repr__ method.
        """
        d1 = Detection("test", 0.5, Box(0.0, 0.0, 10.0, 10.0, 0.0, ScaleFactor(1.0, 1.0)), None)
        assert_ignore_whitespace_string_equal(repr(d1), "Detection(box=Box(cx=0.0, cy=0.0, width=10.0, height=10.0, angle=0.0, scale_factor=ScaleFactor(x=1.0, y=1.0)), label=test, confidence=0.5, mask=None)")
    
    def test_to_dict(self):
        """
        Test the to_dict method.
        """
        d1 = Detection("test", 0.5, Box(0.0, 0.0, 10.0, 10.0, 0.0, ScaleFactor(1.0, 1.0)), None)
        d2 = d1.to_dict()
        assert d2["box"]["cx"] == 0.0
        assert d2["box"]["cy"] == 0.0
        assert d2["box"]["width"] == 10.0
        assert d2["box"]["height"] == 10.0
        assert d2["box"]["angle"] == 0.0
        assert d2["label"] == "test"
        assert d2["confidence"] == 0.5
        assert d2["mask"] is None
        assert d2["box"]["scale_factor"]["x"] == 1.0
        assert d2["box"]["scale_factor"]["y"] == 1.0
    