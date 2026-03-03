from controller import Robot
import time
import random

# =========================
# FSM Definition
# =========================
class RobotState:
    PATROL = 0
    HUMAN_DETECTED = 1
    CAPTURE_IMAGE = 2
    SEND_ALERT = 3

class PatrolFSM:
    def __init__(self):
        self.state = RobotState.PATROL
        self.state_start = time.time()
        self.detection_counter = 0

    def time_in_state(self):
        return time.time() - self.state_start

    def transition(self, new_state):
        print(f"Transition → {new_state}")
        self.state = new_state
        self.state_start = time.time()
        self.detection_counter = 0

    def update(self, human_detected):
        if self.state == RobotState.PATROL:
            if human_detected:
                self.detection_counter += 1
            else:
                self.detection_counter = 0

            if self.detection_counter >= 2:
                self.transition(RobotState.HUMAN_DETECTED)

        elif self.state == RobotState.HUMAN_DETECTED:
            if self.time_in_state() > 2:
                self.transition(RobotState.CAPTURE_IMAGE)

        elif self.state == RobotState.CAPTURE_IMAGE:
            if self.time_in_state() > 1:
                self.transition(RobotState.SEND_ALERT)

        elif self.state == RobotState.SEND_ALERT:
            if self.time_in_state() > 1:
                self.transition(RobotState.PATROL)

# =========================
# Webots Setup
# =========================
robot = Robot()
timestep = int(robot.getBasicTimeStep())

left_motor = robot.getDevice("left_wheel_hinge")
right_motor = robot.getDevice("right_wheel_hinge")

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

camera = robot.getDevice("camera")
camera.enable(timestep)

fsm = PatrolFSM()

# =========================
# Fake human detection (for now)
# =========================
def detect_human():
    return random.random() < 0.05

# =========================
# Main Loop
# =========================
while robot.step(timestep) != -1:

    human_detected = detect_human()
    fsm.update(human_detected)

    # === STATE ACTIONS ===
    if fsm.state == RobotState.PATROL:
        left_motor.setVelocity(5.0)
        right_motor.setVelocity(5.0)

    elif fsm.state == RobotState.HUMAN_DETECTED:
        left_motor.setVelocity(0.0)
        right_motor.setVelocity(0.0)

    elif fsm.state == RobotState.CAPTURE_IMAGE:
        camera.saveImage("capture.jpg", 100)
        left_motor.setVelocity(0.0)
        right_motor.setVelocity(0.0)

    elif fsm.state == RobotState.SEND_ALERT:
        print("Alert Sent!")
        left_motor.setVelocity(0.0)
        right_motor.setVelocity(0.0)
