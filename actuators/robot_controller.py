from actuators.motors import MotorController


class RobotController:

    def __init__(self):
        self.motors = MotorController()

    def patrol(self):
        # continuous forward motion
        self.motors.forward(0.2)

    def investigate(self):
        # stop when human detected
        self.motors.stop()

    def capture_image(self):
        print("Capturing image...")

    def send_alert(self):
        print("Sending alert...")