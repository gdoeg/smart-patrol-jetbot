import time
from fsm import PatrolFSM
from sensors import detect_human


def main():
    fsm = PatrolFSM()

    while True:
        human_detected = detect_human()
        fsm.update(human_detected=human_detected)
        time.sleep(2)


if __name__ == "__main__":
    main()