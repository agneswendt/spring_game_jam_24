import numpy as np
from circle import Circle


class TopHat:
    def __init__(self, top_radius=1.2, bottom_radius=1.2, hat_height=2.0):
        self.mass = 1
        self.inertia = np.eye(3) * 2
        self.inertia_inv = np.linalg.inv(self.inertia)
        self.pos = np.zeros(3)
        self.rot = np.eye(3)
        self.lin_mom = np.zeros(3)
        self.ang_mom = np.zeros(3)

        self.height = hat_height

        self.circles = []
        self.circles.append(Circle(np.array([0, self.height / 2, 0]), top_radius))
        self.circles.append(Circle(np.array([0, -self.height / 2, 0]), bottom_radius))

    def top_circle(self):
        return self.circles[0]

    def bottom_circle(self):
        return self.circles[1]

    def reset(self):
        self.pos = np.zeros(3)
        self.rot = np.eye(3)
        self.lin_mom = np.zeros(3)
        self.ang_mom = np.zeros(3)
