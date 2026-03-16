import time
import random
from actuators.motors import MotorController


class RobotController:

    def __init__(self):
        self.motors = MotorController()

    # --------------------------------
    # Patrol Behavior
    # --------------------------------
    def patrol(self):

        print("Patrolling route...", flush=True)

        # Add slight randomness so patrol paths do not stay perfectly linear.
        if random.random() < 0.12:

            turn_dir = random.choice(["left", "right"])
            turn_duration = random.uniform(0.20, 0.45)

            print(f"Adjusting direction: {turn_dir}", flush=True)

            if turn_dir == "left":
                self.motors.left(0.30, duration=turn_duration)
            else:
                self.motors.right(0.30, duration=turn_duration)

        # Continue forward patrol
        self.motors.forward(0.22)

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
        turn_duration = random.uniform(0.35, 0.65)

        print(f"Obstacle avoidance turn: {turn_dir}", flush=True)

        if turn_dir == "left":
            self.motors.left(0.35, duration=turn_duration)
        else:
            self.motors.right(0.35, duration=turn_duration)

        # Step 4: Resume patrol motion
        self.motors.forward(0.22)