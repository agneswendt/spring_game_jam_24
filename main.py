import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation as R
from ursina import DirectionalLight, EditorCamera, Entity, Sky, Ursina, Vec3, color
from ursina.models.procedural.cylinder import Circle, Cone, Cylinder
from ursina.shaders import lit_with_shadows_shader

import physics
from hand_tracker import HandTracker
from tophat import TopHat

# create a window
app = Ursina()
ed = EditorCamera()
ed.y = 10
ed.z = -50
ed.look_at(-ed.position + Vec3(0, 5, 0))

TOT_X, TOT_Y = 10, 8

physics.th = TopHat(top_radius=1.4, bottom_radius=2, hat_height=2.6)

miny = 0
for circle in physics.th.circles:
    y = circle.pos[1]
    if y < miny:
        miny = y

physics.th.pos[1] = -miny

physics.th.rot = R.from_euler("x", 0, degrees=True).as_matrix()
# physics.th.lin_mom = np.array([0.0, 0.0, -10.0])

# player = Entity(model=Cylinder(radius=1.2, start=-0.5), color=color.orange, scale_y=2)
# DirectionalLight()
background = Entity(
    model="quad", scale=(100, 100 * 0.75), texture="background.png", z=12
)
background = Entity(
    model="quad",
    scale=(100, 100 * 0.75),
    texture="background_top.png",
    y=100 * 0.75 / 2,
    z=12 - 100 * 0.75 / 2,
    rotation_x=-90,
)
player = Entity(
    model="tophat2.obj",
    color=color.gray,
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
# box = Entity(
#     model="cube",
#     color=color.red,
#     scale=(10, 0.5, 10),
#     position=(0, -2.5, 0),
# )
table = Entity(
    model="quad", texture="table.png", scale=(30 * 0.41, 30), position=(0, 0, 3)
)
table.rotation_x = 90
table.rotation_y = 90
wand = Entity(
    model=Cylinder(radius=0.1),
    color=color.blue,
    scale_y=2,
)
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
        ed.look_at(-ed.position + player.position)
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
        physics.th.pos[1] = -miny
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
