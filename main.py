import numpy as np
from scipy.spatial.transform import Rotation as R
from ursina import (
    DirectionalLight,
    EditorCamera,
    Entity,
    Sky,
    Ursina,
    Vec3,
    color,
    audio,
)
from ursina.models.procedural.cylinder import Circle, Cone, Cylinder
from ursina.shaders import lit_with_shadows_shader
from random import randint

import physics
from hand_tracker import HandTracker
from mouse_tracker import MouseTracker
from tophat import TopHat
from screens import MainMenu

# constants
GAME_STATES = ["MENU", "PLAYING"]
USE_MOUSE = False

# global variables
current_game_state = GAME_STATES[0]
flicked = False

app = Ursina()

if USE_MOUSE:
    tracker = MouseTracker(app)
else:
    tracker = HandTracker(show_video=False)

main_menu = None

# create a window
ed = EditorCamera()
physics.th = TopHat(top_radius=1.4, bottom_radius=2, hat_height=2.6)
physics.th.rot = R.from_euler("x", 0, degrees=True).as_matrix()

# instantiate entities
ed.y = 10
ed.z = -50
TOT_X, TOT_Y = 10, 8


miny = 0
for circle in physics.th.circles:
    y = circle.pos[1]
    if y < miny:
        miny = y

physics.th.pos[1] = -miny

physics.th.rot = R.from_euler("x", 0, degrees=True).as_matrix()

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
# player.position = physics.th.pos
player.rotation = R.from_matrix(physics.th.rot).as_euler("xyz", degrees=True)

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


def start_game():
    global current_game_state, main_menu
    current_game_state = "PLAYING"
    print("Starting game main")
    main_menu.visible = False


def add_menu_once():
    global main_menu
    if not main_menu:
        main_menu = MainMenu(start_game)
    else:
        main_menu.visable = True


ed.look_at(-ed.position + player.position)


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

    if flicked:
        physics.update(1 / 60)
        player.position = physics.th.pos
        rot = R.from_matrix(physics.th.rot).as_euler("xyz", degrees=True)
        xf = player.rotation[0]
        xn = rot[0]

        diff = np.round(((xn - xf) / 180)) * 180
        rot[0] = xn + diff

        player.rotation = rot
        ed.look_at(-ed.position + player.position)
    else:
        speed = tracker.process_frame()
        x, y, r_x = tracker.get_wand_pos()
        z = -10
        wand.position = (x, y, z)
        if speed:
            flicked = True
            play_audio(speed)
            strength = speed * 1 / 60
            h = r_x * 2 - 1
            physics.give_impulse(strength, h, 1 / 60)


# update loop for the game
def update():
    global main_menu, current_game_state
    if current_game_state == "MENU":
        add_menu_once()
    elif current_game_state == "PLAYING":
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
            ed.look_at(-ed.position + player.position)
        else:
            speed = tracker.process_frame()
            x, y, r_x = tracker.get_wand_pos()
            z = -10
            wand.position = (x, y, z)
            if speed:
                flicked = True
                play_audio(speed)
                strength = speed * 1 / 60
                h = r_x * 2 - 1
                physics.give_impulse(strength, h, 1 / 60)


# input loop for the game
def input(key):
    global flicked, USE_MOUSE, main_menu, current_game_state
    if key == "space":
        physics.th.reset()
        physics.th.pos[1] = -miny
        flicked = False
        player.position = physics.th.pos
        player.rotation = R.from_matrix(physics.th.rot).as_euler("xyz", degrees=True)
        ed.look_at(-ed.position + player.position)
    if key == "m":
        USE_MOUSE = not USE_MOUSE
        global tracker
        if USE_MOUSE:
            tracker = MouseTracker(app)
        else:
            tracker = HandTracker(show_video=False)
    if key == "escape":
        if current_game_state == "PLAYING":
            current_game_state = "MENU"
            main_menu.visible = True
        else:
            current_game_state = "PLAYING"
            main_menu.visible = False


# start running the game
app.run()
