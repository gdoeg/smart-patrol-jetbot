from jetbot import Robot
import time


class MotorController:
    def __init__(self):
        self.robot = Robot()

    def forward(self, speed=0.2, duration=None):
        self.robot.forward(speed)
        if duration:
            time.sleep(duration)
            self.stop()

    def backward(self, speed=0.2, duration=None):
        self.robot.backward(speed)
        if duration:
            time.sleep(duration)
            self.stop()

    def left(self, speed=0.2, duration=None):
        self.robot.left(speed)
        if duration:
            time.sleep(duration)
            self.stop()

    def right(self, speed=0.2, duration=None):
        self.robot.right(speed)
        if duration:
            time.sleep(duration)
            self.stop()

    def stop(self):
        self.robot.stop()