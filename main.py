from ursina import *
import physics
from scipy.spatial.transform import Rotation as R
from ursina.models.procedural.cylinder import Cylinder
import numpy as np
from hand_tracker import HandTracker
from tophat import TopHat
import matplotlib.pyplot as plt

# create a window
app = Ursina()

TOT_X, TOT_Y = 10, 8

physics.th.rot = R.from_euler("x", -10, degrees=True).as_matrix()
# physics.th.lin_mom = np.array([0.0, 0.0, -10.0])

player = Entity(model=Cylinder(radius=1.2, start=-0.5), color=color.orange, scale_y=2)
box = Entity(model="cube", color=color.red, scale=(10, 0.5, 10), position=(0, -2.5, 0))
wand = Entity(model=Cylinder(radius=0.1), color=color.blue, scale_y=2)
wand.rotation = (45, 0, 0)

HandTracker = HandTracker(show_video=False)

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
        speed = HandTracker.process_frame()
        r_x, r_y = HandTracker.get_hand_pos()
        r_x = r_x * 2
        x, y, z = -(r_x * TOT_X - TOT_X // 2), -(r_y * TOT_Y - TOT_Y // 2 + 1), -10
        wand.position = (x, y, z)
        if speed:
            print(f"Speed of the flick: {speed}")
            print(physics.th.circles[1].pos)
            flicked = True
            strength = speed * 1 / 60
            h = r_x * 2 - 1
            physics.give_impulse(strength, h, 1 / 60)


def input(key):
    global flicked, xr, yr, zr
    if key == "space":
        physics.th.reset()
        flicked = False
        player.position = physics.th.pos
        player.rotation = R.from_matrix(physics.th.rot).as_euler("xyz", degrees=True)
        xr = []
        yr = []
        zr = []
    if key == "escape":
        plt.plot(xr, label="x")
        plt.plot(yr, label="y")
        plt.plot(zr, label="z")
        plt.legend()
        plt.show()


# start running the game
app.run()
