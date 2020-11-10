# This class represents a two dimensional vector.
# TODO:
# - Add the comparison methods from
#   https://difyel.com/python/operators/comparison-in-python-a-tutorial/
# - normalize to value method
# - initialize from tuple
import math


class Vector2D():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calc_rotation(self):
        """Returns the angle between (0,0) and vector in degrees."""
        newtheta = math.atan2(self.y, self.x)
        return math.degrees(newtheta)

    def normalize_vector(self):
        """Normalizes the vector to magnitude zero."""
        magnitude = self.get_magnitude()
        if magnitude == 0:
            return self
        else:
            return(self.x/magnitude, self.y/magnitude)

    def scale_vector(self, scale):
        """Scales the vector by the given quantity."""
        self.x *= scale
        self.y *= scale

    def get_magnitude(self):
        """Returns the magnitude of the vector."""
        return math.sqrt(self.x**2 + self.y**2)
