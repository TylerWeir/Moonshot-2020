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

    def calc_angle(self):
        """Returns the angle between (0,0) and vector in degrees."""
        newtheta = math.atan2(self.y, self.x)
        return 180 - math.degrees(newtheta)

    def normalize(self):
        """Normalizes the vector to magnitude zero."""
        magnitude = self.calc_magnitude()
        if magnitude != 0:
            self.x = self.x/magnitude
            self.y = self.y/magnitude

    def scale(self, scale):
        """Scales the vector by the given quantity."""
        self.x *= scale
        self.y *= scale

    def calc_magnitude(self):
        """Returns the magnitude of the vector."""
        return math.sqrt(self.x**2 + self.y**2)

    def to_tuple(self):
        """Returns the vector as a tuple."""
        return (self.x, self.y)

    def add(self, vector):
        """Adds vector to self."""
        self.x += vector.x
        self.y += vector.y

    def add_values(self, x, y):
        """Adds values to self."""
        self.x += x
        self.y += y

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"
