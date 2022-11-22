import pytest
from dtrack.util import geometry

class TestGeometry:
    """
    Test the geometry module.
    """

    def test_rotate_point(self):
        """
        Test the rotate_point function.
        """
        point = (0, 0)
        angle = 90
        centre = (0, 0)
        assert pytest.approx(geometry.rotate_point(*point, *centre, angle), 0.0001) == (0, 0)

        point = (0, 0)
        angle = 90
        centre = (1, 1)
        assert pytest.approx(geometry.rotate_point(*point, *centre, angle), 0.0001) == (2, 0)

        point = (0, 0)
        angle = 90
        centre = (1, 1)
        assert pytest.approx(geometry.rotate_point(*point, *centre, angle), 0.0001) == (2, 0)

        point = (0, 0)
        angle = 180
        centre = (0, 0)
        assert pytest.approx(geometry.rotate_point(*point, *centre, angle), 0.0001) == (0, 0)

        point = (0, 0)
        angle = 180
        centre = (1, 1)
        assert pytest.approx(geometry.rotate_point(*point, *centre, angle), 0.0001) == (2, 2)

        point = (0, 0)
        angle = 270
        centre = (0, 0)
        assert pytest.approx(geometry.rotate_point(*point, *centre, angle), 0.0001) == (0, 0)

        point = (0, 0)
        angle = 270
        centre = (1, 1)
        assert pytest.approx(geometry.rotate_point(*point, *centre, angle), 0.0001) == (0, 2)

        point = (0, 0)
        angle = 360
        centre = (0, 0)
        assert pytest.approx(geometry.rotate_point(*point, *centre, angle), 0.0001) == (0, 0)

        point = (0, 0)
        angle = 360
        centre = (1, 1)
        assert pytest.approx(geometry.rotate_point(*point, *centre, angle), 0.0001) == (0, 0)
