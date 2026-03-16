from fsm import PatrolFSM
from controllers.robot_controller import RobotController
from sensors.vision import detect_person
from sensors.obstacle import obstacle_detected

import time


controller = RobotController()
fsm = PatrolFSM(controller)


while True:

    inputs = {
        "human_detected": detect_person(),
        "obstacle_detected": obstacle_detected()
    }

    fsm.update(inputs)

    time.sleep(0.1)