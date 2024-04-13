from cvzone.HandTrackingModule import HandDetector
import cv2
import time

SCREEN_X = 1300
SCREEN_Y = 800

class HandTracker:
    def __init__(self, show_video: bool = False, data_points: bool = 6) -> None:
        self.detector = HandDetector(
            staticMode=False,
            maxHands=1,
            modelComplexity=1,
            detectionCon=0.5,
            minTrackCon=0.5,
        )
        self.show_video = show_video
        self.data_points = data_points
        self.finger_pos = []  # (time, (x, y))
        self.cap = cv2.VideoCapture(0)
        self.counter = 0
        self.reset = True

    def calc_speed(self, img) -> int:
        """Return the average speed of the latest data points."""
        speeds = []
        for i in range(
            len(self.finger_pos) - self.data_points, len(self.finger_pos) - 1
        ):
            dt = self.finger_pos[i + 1][0] - self.finger_pos[i][0]
            dist, _, _ = self.detector.findDistance(
                self.finger_pos[i][1], self.finger_pos[i + 1][1], img=img
            )
            speeds.append(dist / dt)
        return sum(speeds) / len(speeds)

    def process_frame(self) -> int | None:
        """
        Process the latest frame. Return the speed of the finger movement if a flick is completed,
        else return None.
        """
        _, img = self.cap.read()
        hands, img = self.detector.findHands(img, draw=True, flipType=True)

        if self.show_video:
            cv2.imshow("Image", img)

        if hands:
            hand1 = hands[0]
            lmList1 = hand1["lmList"]
            x, y = lmList1[8][0:2]
            self.finger_pos.append((time.time(), (x, y)))

            if y < SCREEN_Y // 2:
                self.counter += 1
                if self.counter >= self.data_points and self.reset is True:
                    self.reset = False
                    return self.calc_speed(img)
            else:
                self.counter = 0
                self.reset = True
        
    def get_hand_pos(self) -> tuple[int, int]:
        """Return the coordinates of the finger as a fraction of the screen size.
        """
        if not self.finger_pos:
            return 0.5, 0.5
        x, y = self.finger_pos[-1][1]
        return x / SCREEN_X, y / SCREEN_Y


if __name__ == "__main__":
    hand_tracker = HandTracker(show_video=True)
    while True:
        speed = hand_tracker.process_frame()
        if speed:
            print(speed)
        cv2.waitKey(1)
