import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation as R
from ursina import *
from ursina.models.procedural.cylinder import Circle, Cone, Cylinder

import physics
from hand_tracker import HandTracker
from mouse_tracker import MouseTracker
from tophat import TopHat

# create a window
app = Ursina()
ed = EditorCamera()
USE_MOUSE = False
physics.th = TopHat(top_radius=2.2, bottom_radius=2.2, hat_height=1.0)

physics.th.rot = R.from_euler("x", 0, degrees=True).as_matrix()
# physics.th.lin_mom = np.array([0.0, 0.0, -10.0])

# player = Entity(model=Cylinder(radius=1.2, start=-0.5), color=color.orange, scale_y=2)

player = Entity(
    model="tophat",
    texture="hat1_baseColor",
    position=(physics.th.pos[0], physics.th.pos[1], physics.th.pos[2]),
)
top_circle = Entity(
    parent=player,
    model=Circle(
        resolution=16,
        radius=physics.th.top_circle().radius,
        mode="line",
    ),
    position=physics.th.top_circle().pos,
    rotation_x=90,
    color=color.green,
)
bottom_circle = Entity(
    parent=player,
    model=Circle(
        resolution=16,
        radius=physics.th.bottom_circle().radius,
        mode="line",
    ),
    position=physics.th.bottom_circle().pos,
    rotation_x=90,
    color=color.blue,
)
box = Entity(model="cube", color=color.red, scale=(10, 0.5, 10), position=(0, -2.5, 0))
wand = Entity(model=Cylinder(radius=0.1), color=color.blue, scale_y=2)
wand.rotation = (45, 0, 0)

if USE_MOUSE:
    tracker = MouseTracker(app)
else:
    tracker = HandTracker(show_video=False)

flicked = False


player.position = physics.th.pos
player.rotation = R.from_matrix(physics.th.rot).as_euler("xyz", degrees=True)

xr = []
yr = []
zr = []


def update():
    global flicked

    if flicked:
        physics.update(1 / 60)
        player.position = physics.th.pos
        rot = R.from_matrix(physics.th.rot).as_euler("xyz", degrees=True)
        xf = player.rotation[0]
        xn = rot[0]

        diff = np.round(((xn - xf) / 180)) * 180
        rot[0] = xn + diff

        player.rotation = rot
        xr.append(rot[0])
        yr.append(rot[1])
        zr.append(rot[2])
    else:
        speed = tracker.process_frame()
        x, y, r_x = tracker.get_wand_pos()
        z = -10
        wand.position = (x, y, z)
        if speed:
            print(f"Speed of the flick: {speed}")
            print(physics.th.circles[1].pos)
            flicked = True
            strength = speed * 1 / 60
            h = r_x * 2 - 1
            physics.give_impulse(strength, h, 1 / 60)


def input(key):
    global flicked, xr, yr, zr, USE_MOUSE
    if key == "space":
        physics.th.reset()
        flicked = False
        player.position = physics.th.pos
        player.rotation = R.from_matrix(physics.th.rot).as_euler("xyz", degrees=True)
        xr = []
        yr = []
        zr = []
    if key == "m":
        USE_MOUSE = not USE_MOUSE
        global tracker
        if USE_MOUSE:
            tracker = MouseTracker(app)
        else:
            tracker = HandTracker(show_video=False)
    if key == "escape":
        plt.plot(xr, label="x")
        plt.plot(yr, label="y")
        plt.plot(zr, label="z")
        plt.legend()
        plt.show()


# start running the game
app.run()
