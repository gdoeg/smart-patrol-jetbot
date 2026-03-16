import time

try:
    from Adafruit_MotorHAT import Adafruit_MotorHAT
except Exception as e:
    Adafruit_MotorHAT = None
    _MOTORHAT_IMPORT_ERROR = e
else:
    _MOTORHAT_IMPORT_ERROR = None


class MotorController:

    def __init__(self):

        print("Initializing Adafruit MotorHAT motor driver...", flush=True)

        if Adafruit_MotorHAT is None:
            raise RuntimeError(
                f"Could not import Adafruit_MotorHAT: {_MOTORHAT_IMPORT_ERROR}"
            )

        self.mh = Adafruit_MotorHAT(addr=0x60, i2c_bus=1)

        self.left_motor = self.mh.getMotor(1)
        self.right_motor = self.mh.getMotor(2)

        # MOTOR ORIENTATION FIX
        # If robot moves backwards when told forward,
        # invert both motors here
        self.left_dir = -1
        self.right_dir = -1

        print("Adafruit MotorHAT motor driver initialized.", flush=True)

    @staticmethod
    def _speed_to_power(speed):
        speed = max(0.0, min(1.0, float(speed)))
        return int(speed * 255)

    def _run_motor(self, motor, direction):

        if direction > 0:
            motor.run(Adafruit_MotorHAT.FORWARD)
        elif direction < 0:
            motor.run(Adafruit_MotorHAT.BACKWARD)
        else:
            motor.run(Adafruit_MotorHAT.RELEASE)

    def set_speeds(self, left_speed, right_speed):

        left_power = self._speed_to_power(abs(left_speed))
        right_power = self._speed_to_power(abs(right_speed))

        self.left_motor.setSpeed(left_power)
        self.right_motor.setSpeed(right_power)

        left_dir = 1 if left_speed >= 0 else -1
        right_dir = 1 if right_speed >= 0 else -1

        left_dir *= self.left_dir
        right_dir *= self.right_dir

        self._run_motor(self.left_motor, left_dir)
        self._run_motor(self.right_motor, right_dir)

    def forward(self, speed=0.2, duration=None):

        self.set_speeds(speed, speed)

        if duration:
            time.sleep(duration)
            self.stop()

    def backward(self, speed=0.2, duration=None):

        self.set_speeds(-speed, -speed)

        if duration:
            time.sleep(duration)
            self.stop()

    def left(self, speed=0.2, duration=None):

        self.set_speeds(-speed, speed)

        if duration:
            time.sleep(duration)
            self.stop()

    def right(self, speed=0.2, duration=None):

        self.set_speeds(speed, -speed)

        if duration:
            time.sleep(duration)
            self.stop()

    def stop(self):

        self.left_motor.setSpeed(0)
        self.right_motor.setSpeed(0)

        self.left_motor.run(Adafruit_MotorHAT.RELEASE)
        self.right_motor.run(Adafruit_MotorHAT.RELEASE)