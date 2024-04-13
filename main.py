from ursina import *
import physics
from scipy.spatial.transform import Rotation as R
from ursina.models.procedural.cylinder import Cylinder
import numpy as np
from hand_tracker import HandTracker

# create a window
app = Ursina()

TOT_X, TOT_Y = 10, 8

physics.th.rot = R.from_euler("z", 30, degrees=True).as_matrix()
physics.th.lin_mom = np.array([3.0, 0.0, 0.0])

player = Entity(model=Cylinder(radius=1.2, start=-0.5), color=color.orange, scale_y=2)
box = Entity(model="cube", color=color.red, scale=(10, 0.5, 10), position=(0, -2.5, 0))
wand = Entity(model=Cylinder(radius=0.1), color=color.blue, scale_y=2)
wand.rotation = (45, 0, 0)

HandTracker = HandTracker(show_video=False)

flicked = False


def update():
    global flicked

    if flicked:
        physics.update(1 / 60)
        player.position = physics.th.pos
        player.rotation = R.from_matrix(physics.th.rot).as_euler("xyz", degrees=True)
    else:
        speed = HandTracker.process_frame()
        r_x, r_y = HandTracker.get_hand_pos()
        x, y, z = -(r_x * TOT_X - TOT_X // 2), -(r_y * TOT_Y - TOT_Y // 2 + 1), -10
        wand.position = (x, y, z)
        if speed:
            print(f"Speed of the flick: {speed}")
            flicked = True


def input(key):
    if key == "space":
        physics.th.pos = np.array([0.0, 0.0, 0.0])
        physics.th.lin_mom = np.array([0.0, 0.0, 0.0])


# start running the game
app.run()
