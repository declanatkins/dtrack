import numpy as np


def rotate_point(x, y, centre_x, centre_y, angle):
    """
    Rotate a point around a centre point by a given angle.
    :param x: x coordinate of the point
    :param y: y coordinate of the point
    :param centre_x: x coordinate of the centre point
    :param centre_y: y coordinate of the centre point
    :param angle: angle to rotate by in degrees
    :return: rotated point
    """
    # Convert to radians
    angle = np.deg2rad(angle)

    # Translate to origin
    x -= centre_x
    y -= centre_y

    # Rotate
    x_new = x * np.cos(angle) - y * np.sin(angle)
    y_new = x * np.sin(angle) + y * np.cos(angle)

    # Translate back
    x_new += centre_x
    y_new += centre_y

    return x_new, y_new