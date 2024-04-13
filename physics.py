from tophat import TopHat
import numpy as np

th = TopHat()

ground = -2

up = np.array([0, 1, 0])
g = 9.8

forces = []
force_locs = []


def update(dt):
    global forces, force_locs
    forces = []
    force_locs = []
    collision()
    Ftot = np.zeros(3)
    Ttot = np.zeros(3)

    # speed and inertia
    v = th.lin_mom / th.mass
    inertia_loc = th.rot @ th.inertia @ th.rot.T
    omega = inertia_loc @ th.ang_mom

    print(len(forces))
    # forces
    F = -g * up * th.mass
    Floc = th.pos - np.array([0, 0, 0])
    Ftot += F + sum(forces)
    Ttot += np.cross(Floc, F) + sum(
        [np.cross(force_locs[i], forces[i]) for i in range(len(forces))]
    )

    # derivative
    Rd = np.cross(np.eye(3), omega * dt) @ th.rot

    # update
    th.pos += v * dt
    th.rot += Rd
    th.lin_mom += Ftot * dt
    th.ang_mom += Ttot * dt

    # ortnormalize
    th.rot = np.linalg.qr(th.rot)[0]


def collision():
    n = th.rot @ up
    l = np.cross(n, up)
    d = np.cross(n, l)
    if np.dot(d, up) > 0:
        d = -d

    collision_points = []
    for circle in th.circles:
        pc = th.pos + th.rot @ circle.pos
        p = pc + circle.radius * d
        if p[1] < ground:
            collision_points.append(p)
    if collision_points:
        Fg = th.mass * g / len(collision_points) * up
        for p in collision_points:
            dist = ground - p[1]
            F = Fg + 100 * dist * up
            forces.append(F)
            force_loc = p - th.pos
            force_locs.append(force_loc)
