from random import randint

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation as R
from ursina import (
    DirectionalLight,
    EditorCamera,
    Entity,
    Sky,
    Text,
    Ursina,
    Vec3,
    audio,
    color,
)
from ursina.models.procedural.cylinder import Circle, Cone, Cylinder
from ursina.shaders import lit_with_shadows_shader

import physics
from hand_tracker import HandTracker
from mouse_tracker import MouseTracker
from tophat import TopHat

# create a window
app = Ursina()
ed = EditorCamera()
ed.y = 10
ed.z = -50
TOT_X, TOT_Y = 10, 8

physics.th = TopHat(top_radius=1.4, bottom_radius=2, hat_height=2.6)
USE_MOUSE = False

miny = 0
maxr = 0
for circle in physics.th.circles:
    y = circle.pos[1]
    if y < miny:
        miny = y
    r = circle.radius
    if r > maxr:
        maxr = r

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
    color=color.black,
    scale_y=2,
)
wandtip1 = Entity(
    parent=wand,
    model=Cylinder(radius=0.1, start=5),
    color=color.white,
    scale_y=0.2,
)
wandtip2 = Entity(
    parent=wand,
    model=Cylinder(radius=0.1, start=-1),
    color=color.white,
    scale_y=0.2,
)
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
ed.look_at(-ed.position + player.position)

win_text = Text(
    "You win!",
    enabled=False,
    position=(0, 0),
    scale=0.1,
    background=True,
    color=color.black,
)


def play_audio(speed):
    ranges = {
        (0, 200): "slow.mp3",
        (200, 600): "mediumslow.mp3",
        (600, 1000): "medium.mp3",
        (1000, 1600): "mediumfast.mp3",
        (1600, 2500): "fast.mp3",
        (2500, 1000000): "oh-my-god-meme.mp3",
    }
    for r in ranges:
        if r[0] <= speed <= r[1]:
            a = audio.Audio(ranges[r], autoplay=True, loop=False)
            a.play()
            return


def update():
    global flicked

    if flicked and not physics.is_in_win_state:
        wand.enabled = False
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
        if physics.is_in_win_state:
            print("You win!")
            physics.is_in_win_state = False
            win_text.enabled = True
            win = True
    else:
        speed = tracker.process_frame()
        x, y, r_x = tracker.get_wand_pos()
        z = -10
        wand.position = (x, y, z)
        hit_loc = x / maxr
        if speed and abs(hit_loc) < 1:
            print(f"Speed of the flick: {speed}")
            print(physics.th.circles[1].pos)
            flicked = True
            play_audio(speed)
            strength = speed * 1 / 60
            physics.give_impulse(strength, hit_loc, 1 / 60)


def input(key):
    global flicked, xr, yr, zr, USE_MOUSE
    if key == "space":
        physics.th.reset()
        physics.th.pos[1] = -miny
        flicked = False
        player.position = physics.th.pos
        player.rotation = R.from_matrix(physics.th.rot).as_euler("xyz", degrees=True)
        ed.look_at(-ed.position + player.position)
        wand.enabled = True
        physics.is_in_win_state = False
        win_text.enabled = False
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
