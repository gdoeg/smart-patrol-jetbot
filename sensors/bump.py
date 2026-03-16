import Jetson.GPIO as GPIO

BUMP_PIN = 17   # change depending on wiring

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUMP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def detect_bump():

    if GPIO.input(BUMP_PIN) == GPIO.LOW:
        print("⚠️ BUMP DETECTED")
        return True

    return False