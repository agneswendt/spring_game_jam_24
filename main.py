from ursina import *
import physics
from scipy.spatial.transform import Rotation as R
from ursina.models.procedural.cylinder import Cylinder
import numpy as np

# create a window
app = Ursina()

# most things in ursina are Entities. An Entity is a thing you place in the world.
# you can think of them as GameObjects in Unity or Actors in Unreal.
# the first parameter tells us the Entity's model will be a 3d-model called 'cube'.
# ursina includes some basic models like 'cube', 'sphere' and 'quad'.

# the next parameter tells us the model's color should be orange.

# 'scale_y=2' tells us how big the entity should be in the vertical axis, how tall it should be.
# in ursina, positive x is right, positive y is up, and positive z is forward.

physics.th.rot = R.from_euler("z", 30, degrees=True).as_matrix()
physics.th.lin_mom = np.array([3.0, 0.0, 0.0])

player = Entity(model=Cylinder(radius=1.2, start=-0.5), color=color.orange, scale_y=2)
box = Entity(model="cube", color=color.red, scale=(10, 0.5, 10), position=(0, -2.5, 0))

# create a function called 'update'.
# this will automatically get called by the engine every frame.

# print(R.from_euler("z", 180, degrees=True).as_matrix())
# print(R.from_euler("z", 0, degrees=True).as_matrix())
# exit()

inc = 0


def update():
    # global inc
    # inc += 1
    # physics.th.rot = R.from_euler("z", inc, degrees=True).as_matrix()
    physics.update(1 / 60)
    player.position = physics.th.pos
    player.rotation = R.from_matrix(physics.th.rot).as_euler("xyz", degrees=True)


# this part will make the player move left or right based on our input.
# to check which keys are held down, we can check the held_keys dictionary.
# 0 means not pressed and 1 means pressed.
# time.dt is simply the time since the last frame. by multiplying with this, the
# player will move at the same speed regardless of how fast the game runs.


def input(key):
    if key == "space":
        physics.th.pos = np.array([0.0, 0.0, 0.0])
        physics.th.lin_mom = np.array([0.0, 0.0, 0.0])


# start running the game
app.run()
