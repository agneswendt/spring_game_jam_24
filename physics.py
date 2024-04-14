import numpy as np

from tophat import TopHat

th = TopHat()

ground = 0

up = np.array([0, 1, 0])
g = 9.8

forces = []
force_locs = []

has_collided = False


def give_impulse(strength, h, dt):
    global forces, force_locs
    forces = []
    force_locs = []
    forces.append(strength * up / dt)
    circ = th.circles[1]
    loc = circ.pos.copy()
    loc[0] += h * circ.radius
    loc[2] += circ.radius
    # print("Flick at", h)
    force_locs.append(loc)


def update(dt):
    global forces, force_locs
    collision(dt)
    Ftot = np.zeros(3)
    Ttot = np.zeros(3)

    # speed and inertia
    v = th.lin_mom / th.mass
    inertia_loc = th.rot @ th.inertia_inv @ th.rot.T
    omega = inertia_loc @ th.ang_mom

    # forces
    F = -g * up * th.mass
    Floc = np.array([0, 0, 0])
    Ftot += F + sum(forces)
    Ttot += np.cross(Floc, F) + sum(
        [np.cross(force_locs[i], forces[i]) for i in range(len(forces))]
    )
    forces = []
    force_locs = []

    # derivative
    Rd = np.cross(np.eye(3), omega * dt) @ th.rot

    # update
    th.pos += v * dt
    th.rot += Rd
    th.lin_mom += Ftot * dt
    th.ang_mom += Ttot * dt
    th.ang_mom *= 0.99

    # ortnormalize
    th.rot = np.linalg.qr(th.rot)[0]

    # flip determinant if needed
    if np.linalg.det(th.rot) < 0:
        th.rot = -th.rot


counter = 0


def collision(dt):
    global has_collided
    global counter
    n = th.rot @ up
    l = np.cross(n, up)
    d = np.cross(n, l)
    if np.dot(d, up) > 0:
        d = -d

    points = []
    for circle in th.circles:
        pc = th.pos + th.rot @ circle.pos
        p = pc + circle.radius * d
        points.append((p, p[1] < ground, pc))
    num_collisions = sum([p[1] for p in points])
    if num_collisions > 0:
        counter += 1
        # print("collision", counter)
        mom = th.lin_mom[1]
        # fac = 1 - 1 / (1 + abs(mom))
        fac = 0.0
        # print(mom)
        F = -(1 + fac) * mom * up / dt / num_collisions
        # F2 = th.mass * g * up / len(collision_points)
        max_dist = 0
        inertia_loc = th.rot @ th.inertia_inv @ th.rot.T
        omega = inertia_loc @ th.ang_mom
        # print(omega, th.ang_mom)
        for i, (p, collided, circle_center) in enumerate(points):
            if not collided:
                continue

            side1 = p - points[(i + 1) % 2][0]
            side1 = side1 / np.linalg.norm(side1)
            levelness1 = abs(np.dot(side1, up))

            side2 = 2 * (p - circle_center)
            side2 = side2 / np.linalg.norm(side2)
            levelness2 = abs(np.dot(side2, up))

            levelness = min(levelness1, levelness2)

            # levelness = min(1, levelness * 10) ** 3
            ang_mom = np.linalg.norm(th.ang_mom)
            # print(ang_mom, levelness)
            if ang_mom < 1 and levelness < 0.01:
                th.ang_mom = np.zeros(3)

            force_loc = p - th.pos
            # force_loc[::2] *= levelness
            dist = ground - p[1]
            max_dist = max(max_dist, dist)
            if np.dot(F, up) > 0:
                forces.append(F)
                force_locs.append(force_loc)

            v1 = th.lin_mom / th.mass
            #
            maxF1 = np.cross(th.ang_mom, force_loc) / np.linalg.norm(force_loc) ** 2
            maxF2 = th.mass * v1 / dt
            maxF = maxF1 + maxF2
            maxF[1] = 0

            v2 = np.cross(omega, force_loc)
            # print(np.cross(th.ang_mom, force_loc), v)
            v = v1 + v2
            dir = v / (1e-8 + np.linalg.norm(v))
            Ff = -dir * g * th.mass * 2
            # print("Velocity at point of contact:", v)
            # print("Direction of velocity:", dir)
            # print("Frictional force before clipping:", Ff)
            # print("Maximum allowable force:", maxF)
            Ff = np.clip(Ff, -np.abs(maxF), np.abs(maxF))
            # print("Frictional force after clipping:", Ff)
            # Ff = np.clip(Ff, -maxF, maxF)
            # print(maxF, v, Ff)
            forces.append(Ff)
            # forces.append(np.array([2, 0, 0]))
            force_locs.append(force_loc)
            break
        max_dist = min(max_dist, 0.1)
        th.pos += max_dist * up  # - 1 * th.lin_mom / th.mass * dt
        print(max_dist, th.pos, th.circles[0].pos, th.circles[1].pos)
