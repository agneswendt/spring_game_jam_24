from tophat import TopHat
import numpy as np

th = TopHat()

up = np.array([0, 1, 0])
g = 9.8


def update(dt):
    Ftot = np.zeros(3)
    Ttot = np.zeros(3)

    # speed and inertia
    v = th.lin_mom / th.mass
    inertia_loc = th.rot @ th.inertia @ th.rot.T
    omega = inertia_loc @ th.ang_mom

    # forces
    F = -g * up * th.mass
    Floc = th.pos - np.array([0.01, 0, 0])
    Ftot += F
    Ttot += np.cross(Floc, F)

    # derivative
    Rd = np.cross(np.eye(3), omega * dt) @ th.rot
    print(Rd)
    # update
    th.pos += v * dt
    th.rot += Rd + dt
    th.lin_mom += Ftot * dt
    th.ang_mom += Ttot * dt

    # ortnormalize
    th.rot = np.linalg.qr(th.rot)[0]
