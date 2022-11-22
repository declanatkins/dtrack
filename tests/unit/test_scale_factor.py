from dtrack.util.scale_factor import ScaleFactor
from tests.assertions import assert_ignore_whitespace_string_equal

class TestScaleFactor:

    def test_from_json(self):
        """
        Test the from_json method.
        """
        scale_factor = ScaleFactor.from_json("""{
            "x": 10,
            "y": 10
        }""")
        assert scale_factor == ScaleFactor(10, 10)
    
    def test_from_dict(self):
        """
        Test the from_dict method.
        """
        scale_factor = ScaleFactor.from_dict({
            "x": 10,
            "y": 10
        })
        assert scale_factor == ScaleFactor(10, 10)
    
    def test__hash__(self):
        """
        Test the __hash__ method.
        """
        scale_factor = ScaleFactor(10, 10)
        assert hash(scale_factor) == hash((10, 10))
    
    def test_to_dict(self):
        """
        Test the to_dict method.
        """
        scale_factor = ScaleFactor(10, 10)
        assert scale_factor.to_dict() == {
            "x": 10,
            "y": 10
        }
    
    def test_to_json(self):
        """
        Test the to_json method.
        """
        scale_factor = ScaleFactor(10, 10)
        assert_ignore_whitespace_string_equal(scale_factor.to_json(), """{
            "x": 10,
            "y": 10
        }""")
    
    def test__eq__(self):
        """
        Test the __eq__ method.
        """
        scale_factor = ScaleFactor(10, 10)
        assert scale_factor == ScaleFactor(10, 10)
    
    def test__ne__(self):
        """
        Test the __ne__ method.
        """
        scale_factor = ScaleFactor(10, 10)
        assert scale_factor != ScaleFactor(11, 10)
        assert scale_factor != ScaleFactor(10, 11)
        assert scale_factor != ScaleFactor(11, 11)

    def test__str__(self):
        """
        Test the __str__ method.
        """
        scale_factor = ScaleFactor(10, 10)
        assert str(scale_factor) == "ScaleFactor(x=10, y=10)"
    
    def test__repr__(self):
        """
        Test the __repr__ method.
        """
        scale_factor = ScaleFactor(10, 10)
        assert repr(scale_factor) == "ScaleFactor(x=10, y=10)"
