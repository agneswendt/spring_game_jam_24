import numpy as np


class Circle:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius

    def area(self):
        return 3.14 * self.radius**2

    def perimeter(self):
        return 2 * 3.14 * self.radius
