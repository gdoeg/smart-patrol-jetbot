from fsm import PatrolFSM
from actuators.robot_controller import RobotController

from sensors.vision import detect_person
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

    
        frame = camera.Capture()
        human_detected, vision_obstacle_detected, obstacle_side = detect_person(frame)

        # -----------------------------
        # Bump sensor check
        # -----------------------------
        bump_detected = detect_bump()


        # -----------------------------
        # Combine obstacle signals
        # -----------------------------
        obstacle_detected = bump_detected or vision_obstacle_detected


        inputs = {
            "human_detected": human_detected,
            "obstacle_detected": obstacle_detected,
            "obstacle_side": obstacle_side
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