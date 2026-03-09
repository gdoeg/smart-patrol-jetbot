import time
from fsm import PatrolFSM
from sensors.vision import detect_human
from actuators.robot_controller import RobotController


def main():

    controller = RobotController()
    fsm = PatrolFSM(controller)

    while True:

        human_detected = detect_human()

        fsm.update({
            "human_detected": human_detected
        })

        time.sleep(2)


if __name__ == "__main__":
    main()