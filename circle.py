import numpy as np


class Circle:
    def __init__(self, pos, radius):
        self._pos = pos
        self.radius = radius

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        raise AttributeError("Cannot set the position of a circle.")
        self._pos = value

    def area(self):
        return 3.14 * self.radius**2

    def perimeter(self):
        return 2 * 3.14 * self.radius
