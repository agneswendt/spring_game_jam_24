from ursina import *


class MainMenu(Entity):
    def __init__(self, start_game_func):
        super().__init__(
            parent=scene, model="quad", texture="menu_screen", scale=10, z=-10
        )

        self.start_button = Button(
            text="Start Game",
            color=color.black,
            scale=(0.2, 0.1),
            position=(-0.2, 0),
        )
        self.settings_button = Button(
            text="Settings",
            color=color.black,
            scale=(0.2, 0.1),
            position=(0, -0.2),
        )
        self.exit_button = Button(
            text="Exit Game",
            color=color.black,
            scale=(0.2, 0.1),
            position=(0.2, 0),
        )

        self.start_game_func = start_game_func
        self.start_button.on_click = self.start_game
        self.exit_button.on_click = application.quit

    def start_game(self):
        print("Starting game from screen")
        self.start_button.enabled = False
        self.settings_button.enabled = False
        self.exit_button.enabled = False
        destroy(self.start_button)
        destroy(self.settings_button)
        destroy(self.exit_button)
        invoke(self.start_game_delayed, delay=0.5)
        self.start_game_func()

    def start_game_delayed(self):
        destroy(self)
