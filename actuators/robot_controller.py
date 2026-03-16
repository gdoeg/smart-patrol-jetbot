from actuators.motors import MotorController
from sensors.vision import detect_person


class RobotController:

    def __init__(self):
        self.motors = MotorController()

    def patrol(self):
        print("Patrolling route...", flush=True)
        self.motors.forward(0.2)

    def investigate(self):
        print("Investigating potential human...", flush=True)
        self.motors.stop()

    def capture_image(self):
        print("Capturing image...", flush=True)
        detect_person()

    def send_alert(self):
        print("Alert already handled by vision system", flush=True)

    def avoid_obstacle(self):
        print("Avoiding obstacle...", flush=True)

        self.motors.backward(0.2)
        time.sleep(0.5)

        self.motors.left(0.3)
        time.sleep(0.5)

        self.motors.forward(0.2)