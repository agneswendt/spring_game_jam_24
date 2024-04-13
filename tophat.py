import numpy as np


class TopHat:
    def __init__(self):
        self.mass = 1
        self.inertia = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.inertia_inv = np.linalg.inv(self.inertia)
        self.center = np.zeros(3)
        self.pos = np.zeros(3)
        self.rot = np.zeros((3, 3))
        self.lin_mom = np.zeros(3)
        self.ang_mom = np.zeros(3)
