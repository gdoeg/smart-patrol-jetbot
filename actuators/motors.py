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

        print("Adafruit MotorHAT motor driver initialized.", flush=True)

    @staticmethod
    def _speed_to_power(speed):
        speed = max(0.0, min(1.0, float(speed)))
        return int(speed * 255)

    def forward(self, speed=0.2, duration=None):
        power = self._speed_to_power(speed)
        self.left_motor.setSpeed(power)
        self.right_motor.setSpeed(power)
        self.left_motor.run(Adafruit_MotorHAT.FORWARD)
        self.right_motor.run(Adafruit_MotorHAT.FORWARD)
        if duration:
            time.sleep(duration)
            self.stop()

    def backward(self, speed=0.2, duration=None):
        power = self._speed_to_power(speed)
        self.left_motor.setSpeed(power)
        self.right_motor.setSpeed(power)
        self.left_motor.run(Adafruit_MotorHAT.BACKWARD)
        self.right_motor.run(Adafruit_MotorHAT.BACKWARD)
        if duration:
            time.sleep(duration)
            self.stop()

    def left(self, speed=0.2, duration=None):
        power = self._speed_to_power(speed)
        self.left_motor.setSpeed(power)
        self.right_motor.setSpeed(power)
        self.left_motor.run(Adafruit_MotorHAT.BACKWARD)
        self.right_motor.run(Adafruit_MotorHAT.FORWARD)
        if duration:
            time.sleep(duration)
            self.stop()

    def right(self, speed=0.2, duration=None):
        power = self._speed_to_power(speed)
        self.left_motor.setSpeed(power)
        self.right_motor.setSpeed(power)
        self.left_motor.run(Adafruit_MotorHAT.FORWARD)
        self.right_motor.run(Adafruit_MotorHAT.BACKWARD)
        if duration:
            time.sleep(duration)
            self.stop()

    def stop(self):
        self.left_motor.run(Adafruit_MotorHAT.RELEASE)
        self.right_motor.run(Adafruit_MotorHAT.RELEASE)