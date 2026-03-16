from fsm import PatrolFSM
from actuators.robot_controller import RobotController

from sensors.vision import detect_person
from sensors.vision_obstacle import detect_obstacle
from sensors.bump import detect_bump

import jetson_utils
import time


# -----------------------------
# Initialize camera
# -----------------------------
camera = jetson_utils.videoSource("csi://0")


# -----------------------------
# Initialize controller + FSM
# -----------------------------
controller = RobotController()
fsm = PatrolFSM(controller)


try:

    while True:

        # -----------------------------
        # HUMAN DETECTION
        # -----------------------------
        human_detected, _ = detect_person(camera)


        # -----------------------------
        # CAMERA OBSTACLE DETECTION
        # -----------------------------
        vision_obstacle = detect_obstacle(camera)


        # -----------------------------
        # FUTURE SENSORS (placeholders)
        # -----------------------------
        bump_detected = detect_bump()


        # -----------------------------
        # Combine obstacle signals
        # -----------------------------
        obstacle_detected = (
            vision_obstacle
            or bump_detected
        )


        inputs = {
            "human_detected": human_detected,
            "obstacle_detected": obstacle_detected
        }


        # -----------------------------
        # Update FSM
        # -----------------------------
        fsm.update(inputs)


        time.sleep(0.1)


except KeyboardInterrupt:
    print("Keyboard interrupt received. Stopping robot motors...")
except Exception as e:
    print(f"Unhandled exception: {e}")
finally:
    controller.stop()