from tophat import TopHat
import numpy as np

th = TopHat()

g = 9.8


def update(dt):
    Ftot = np.zeros(3)
    Ttot = np.zeros(3)

    # speed and inertia
    v = th.lin_mom / th.mass
    inertia_loc = th.rot @ th.inertia @ th.rot.T
    omega = inertia_loc @ th.ang_mom

    # forces
    F = np.array([0, 0, -g]) * th.mass
    Floc = th.pos
    Ftot += F
    Ttot += np.cross(Floc, F)

    # derivative
    Rd = np.cross(np.eye(3), omega * dt) @ th.rot

    # update
    th.pos += v * dt
    th.rot += Rd + dt
    th.lin_mom += Ftot * dt
    th.ang_mom += Ttot * dt

    # ortnormalize
    th.rot = np.linalg.qr(th.rot)[0]
