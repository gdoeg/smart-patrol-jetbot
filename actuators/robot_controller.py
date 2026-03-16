import time
import random
from actuators.motors import MotorController


class RobotController:

    def __init__(self):
        self.motors = MotorController()
        self.forward_duration_sec = 4.0
        self.turn_duration_sec = 0.95
        self.forward_speed = 0.24
        self.turn_speed = 0.30
        self.patrol_segment = "forward"
        self.segment_start_time = time.time()

    def reset_patrol_timing(self):
        self.patrol_segment = "forward"
        self.segment_start_time = time.time()

    # --------------------------------
    # Patrol Behavior (Rectangle Perimeter)
    # --------------------------------
    def patrol(self):
        now = time.time()
        elapsed = now - self.segment_start_time

        print(f"segment={self.patrol_segment} elapsed={elapsed:.2f}", flush=True)

        if self.patrol_segment == "forward":
            print("Rectangle patrol: forward segment...", flush=True)
            self.motors.forward(self.forward_speed)

            if elapsed >= self.forward_duration_sec:
                self.patrol_segment = "turn"
                self.segment_start_time = now

        else:
            print("Rectangle patrol: turning segment...", flush=True)
            self.motors.left(self.turn_speed)

            if elapsed >= self.turn_duration_sec:
                self.patrol_segment = "forward"
                self.segment_start_time = now

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
        self.reset_patrol_timing()

    # --------------------------------
    # Emergency Stop
    # --------------------------------
    def stop(self):

        print("Stopping motors...", flush=True)
        self.motors.stop()