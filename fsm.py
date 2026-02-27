from enum import Enum, auto
import time


class RobotState(Enum):
    IDLE = auto()
    PATROL = auto()
    HUMAN_DETECTED = auto()
    CAPTURE_IMAGE = auto()
    SEND_ALERT = auto()


class PatrolFSM:
    def __init__(self):
        self.state = RobotState.IDLE
        self.state_start_time = time.time()
        self.detection_counter = 0
        print(f"Initial State: {self.state.name}")

    # ------------------------
    # Public Update Method
    # ------------------------
    def update(self, human_detected=False):
        self.handle_transitions(human_detected)
        self.execute_state_action()

    # ------------------------
    # Transition Logic
    # ------------------------
    def handle_transitions(self, human_detected):

        if self.state == RobotState.IDLE:
            self.transition_to(RobotState.PATROL)

        elif self.state == RobotState.PATROL:
            if human_detected:
                self.detection_counter += 1
            else:
                self.detection_counter = 0

            # Require confirmation (2 consecutive detections)
            if self.detection_counter >= 2:
                self.transition_to(RobotState.HUMAN_DETECTED)

        elif self.state == RobotState.HUMAN_DETECTED:
            # Brief investigation period
            if self.time_in_state() > 2:
                self.transition_to(RobotState.CAPTURE_IMAGE)

        elif self.state == RobotState.CAPTURE_IMAGE:
            if self.time_in_state() > 1:
                self.transition_to(RobotState.SEND_ALERT)

        elif self.state == RobotState.SEND_ALERT:
            if self.time_in_state() > 1:
                self.transition_to(RobotState.PATROL)

    # ------------------------
    # Transition Helper
    # ------------------------
    def transition_to(self, new_state):
        print(f"Transition: {self.state.name} → {new_state.name}")
        self.state = new_state
        self.state_start_time = time.time()
        self.detection_counter = 0

    # ------------------------
    # State Actions
    # ------------------------
    def execute_state_action(self):

        if self.state == RobotState.PATROL:
            print("Patrolling route...")

        elif self.state == RobotState.HUMAN_DETECTED:
            print("Investigating potential human...")

        elif self.state == RobotState.CAPTURE_IMAGE:
            print("Capturing image from camera...")

        elif self.state == RobotState.SEND_ALERT:
            print("Sending alert to monitoring system...")

        print(f"Current State: {self.state.name}\n")

    # ------------------------
    # Utility
    # ------------------------
    def time_in_state(self):
        return time.time() - self.state_start_time