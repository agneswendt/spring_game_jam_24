from ursina import *
import time

SCREEN_X = 1.6
SCREEN_Y = 1
TOT_X, TOT_Y = 10, 8


class MouseTracker:
    def __init__(self, app, data_points=4) -> None:
        self.mouse = app.mouse
        self.mouse_pos = []  # (time, (x, y))
        self.counter = 0
        self.data_points = data_points
        self.reset = True

    def calc_speed(self) -> int:
        """Return the average speed of the latest data points."""
        speeds = []
        for i in range(len(self.mouse_pos) - self.data_points, len(self.mouse_pos) - 1):
            dt = self.mouse_pos[i + 1][0] - self.mouse_pos[i][0]
            dist = self.mouse_pos[i + 1][1][1] - self.mouse_pos[i][1][1]
            speeds.append(dist / dt)
        return sum(speeds) * 40 / len(speeds)

    def process_frame(self) -> int | None:
        """
        Process the latest frame. Return the speed of the mouse movement if a flick is completed,
        else return None.
        """
        x, y, _ = self.get_wand_pos()
        if (x, y) != (0, 0):
            self.mouse_pos.append((time.time(), (x, y)))

            if y > 0:
                self.counter += 1
                if self.counter >= self.data_points and self.reset is True:
                    self.reset = False
                    return self.calc_speed()
            else:
                self.counter = 0
                self.reset = True

    def get_wand_pos(self) -> tuple[int, int]:
        x, y = self.mouse.x / SCREEN_X, self.mouse.y / SCREEN_Y
        return 10 * x, 8 * y, (self.mouse.x + 0.8) / 1.6


if __name__ == "__main__":
    pass
