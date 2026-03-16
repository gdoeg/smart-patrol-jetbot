import random
from actuators.motors import MotorController


class RobotController:

    def __init__(self):
        self.motors = MotorController()

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

        self.motors.forward(0.22)

    def avoid_obstacle(self):

        print("Avoiding obstacle...", flush=True)

        # Back away, rotate, then continue patrol motion.
        self.motors.backward(0.22, duration=0.35)

        turn_dir = random.choice(["left", "right"])
        turn_duration = random.uniform(0.35, 0.65)

        print(f"Obstacle avoidance turn: {turn_dir}", flush=True)
        if turn_dir == "left":
            self.motors.left(0.35, duration=turn_duration)
        else:
            self.motors.right(0.35, duration=turn_duration)

        self.motors.forward(0.22)