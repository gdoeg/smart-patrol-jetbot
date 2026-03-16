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
vision_obstacle_frames = 0
VISION_OBSTACLE_FRAMES = 3


try:

    while True:

    
        frame = camera.Capture()
        human_detected, _ = detect_person(frame)
        vision_obstacle_raw = detect_obstacle(frame)

        if vision_obstacle_raw:
            vision_obstacle_frames += 1
        else:
            vision_obstacle_frames = 0

        vision_obstacle = vision_obstacle_frames >= VISION_OBSTACLE_FRAMES

        # -----------------------------
        # Bump sensor check
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