import time
import random
from actuators.motors import MotorController


class RobotController:

    def __init__(self):
        self.motors = MotorController()

    # --------------------------------
    # Patrol Behavior (Wall-Following)
    # --------------------------------
    def patrol(self):

        print("Wall-follow patrol...", flush=True)

        # Base forward speed
        base_speed = 0.24

        # Small steering drift so robot slowly curves
        drift = random.uniform(-0.03, 0.03)

        left_speed = base_speed + drift
        right_speed = base_speed - drift

        # Clamp speeds so they stay safe
        left_speed = max(0.18, min(0.30, left_speed))
        right_speed = max(0.18, min(0.30, right_speed))

        # Apply the speeds
        self.motors.set_speeds(left_speed, right_speed)

    # --------------------------------
    # Obstacle Avoidance
    # --------------------------------
    def avoid_obstacle(self):

        print("Avoiding obstacle...", flush=True)

        # Step 1: Back away from obstacle
        self.motors.backward(0.25, duration=0.6)

        # Step 2: Small pause so robot fully clears obstacle
        time.sleep(0.2)

        # Step 3: Randomly turn away
        turn_dir = random.choice(["left", "right"])
        turn_duration = random.uniform(0.30, 0.50)

        print(f"Obstacle avoidance turn: {turn_dir}", flush=True)

        if turn_dir == "left":
            self.motors.left(0.35, duration=turn_duration)
        else:
            self.motors.right(0.35, duration=turn_duration)

        # Step 4: Resume forward motion
        self.motors.forward(0.22)

    # --------------------------------
    # Emergency Stop
    # --------------------------------
    def stop(self):

        print("Stopping motors...", flush=True)
        self.motors.stop()