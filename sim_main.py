import random
import time

from fsm import PatrolFSM
from sim_controller import SimRobotController


def generate_sim_inputs():
    return {
        "human_detected": random.random() < 0.05,
        "obstacle_detected": random.random() < 0.1,
        "obstacle_side": random.choice(["left", "right", None]),
    }


def main():
    controller = SimRobotController()
    fsm = PatrolFSM(controller)

    try:
        while True:
            inputs = generate_sim_inputs()
            print(f"SIM INPUTS: {inputs}", flush=True)
            fsm.update(inputs)
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("SIM: keyboard interrupt, stopping simulation", flush=True)
    finally:
        controller.stop()


if __name__ == "__main__":
    main()
