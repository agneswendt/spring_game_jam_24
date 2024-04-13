import numpy as np
from circle import Circle


class TopHat:
    def __init__(self):
        self.mass = 1
        self.inertia = np.eye(3) * 2
        self.inertia_inv = np.linalg.inv(self.inertia)
        self.center = np.zeros(3)
        self.pos = np.zeros(3)
        self.rot = np.eye(3)
        self.lin_mom = np.zeros(3)
        self.ang_mom = np.zeros(3)

        self.circles = []
        self.circles.append(Circle(np.array([0, 1, 0]), 1.2))
        self.circles.append(Circle(np.array([0, -1, 0]), 1.2))
