from fsm import PatrolFSM
from actuators.robot_controller import RobotController
from sensors.vision import detect_person

import time


controller = RobotController()
fsm = PatrolFSM(controller)


while True:

    human_detected, obstacle_detected = detect_person()

    inputs = {
        "human_detected": human_detected,
        "obstacle_detected": obstacle_detected
    }

    fsm.update(inputs)

    time.sleep(0.1)