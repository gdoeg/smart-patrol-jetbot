import Jetson.GPIO as GPIO
import time

BUMP_PIN = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(BUMP_PIN, GPIO.IN)

last_trigger_time = 0


def detect_bump():

    global last_trigger_time

    state = GPIO.input(BUMP_PIN)

    # Debounce sensor
    if state == GPIO.LOW:

        now = time.time()

        if now - last_trigger_time > 1.0:
            last_trigger_time = now
            print("⚠️ BUMP DETECTED")
            return True

    return False