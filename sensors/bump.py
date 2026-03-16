import Jetson.GPIO as GPIO
import time

BUMP_PIN = 18
DEBOUNCE_SEC = 0.05

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(BUMP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

last_raw_state = GPIO.input(BUMP_PIN)
stable_state = last_raw_state
last_state_change_time = time.time()
collision_latched = False


def detect_bump():

    global last_raw_state, stable_state, last_state_change_time, collision_latched

    now = time.time()
    raw_state = GPIO.input(BUMP_PIN)

    if raw_state != last_raw_state:
        last_raw_state = raw_state
        last_state_change_time = now
        return False

    if raw_state != stable_state and now - last_state_change_time >= DEBOUNCE_SEC:
        stable_state = raw_state

        if stable_state == GPIO.HIGH:
            collision_latched = False
            return False

    if (
        stable_state == GPIO.LOW
        and not collision_latched
        and now - last_state_change_time >= DEBOUNCE_SEC
    ):
        collision_latched = True
        print("⚠️ BUMP DETECTED")
        return True

    return False