from enum import Enum, auto
import time


class RobotState(Enum):
    IDLE = auto()
    PATROL = auto()
    HUMAN_DETECTED = auto()
    CAPTURE_IMAGE = auto()
    SEND_ALERT = auto()


class PatrolFSM:
    def __init__(self, controller):
        self.controller = controller
        self.state = RobotState.IDLE
        self.state_start_time = time.time()
        self.detection_counter = 0
        self.latest_inputs = {}
        print(f"Initial State: {self.state.name}", flush=True)
        self.transition_to(RobotState.PATROL)

    # ------------------------
    # Public Update Method
    # ------------------------
    def update(self, inputs: dict):
        print("FSM UPDATE RUNNING", flush=True)
        """
        inputs example:
        {
            "human_detected": bool,
            "obstacle_detected": bool
        }
        """
        self.latest_inputs = inputs
        self.handle_transitions(inputs)
        self.execute_state_action()

    # ------------------------
    # Transition Logic
    # ------------------------
    def handle_transitions(self, inputs):

        human_detected = inputs.get("human_detected", False)
        obstacle_detected = inputs.get("obstacle_detected", False)

        if self.state == RobotState.IDLE:
            self.transition_to(RobotState.PATROL)

        elif self.state == RobotState.PATROL:
            # Obstacle handling takes priority while patrolling.
            if obstacle_detected:
                self.detection_counter = 0
                return

            if human_detected:
                self.detection_counter += 1
            else:
                self.detection_counter = 0

            if self.detection_counter >= 2:
                self.transition_to(RobotState.HUMAN_DETECTED)

        elif self.state == RobotState.HUMAN_DETECTED:
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
        print(f"Transition: {self.state.name} → {new_state.name}", flush=True)
        self.state = new_state
        self.state_start_time = time.time()
        self.detection_counter = 0

    # ------------------------
    # State Actions
    # ------------------------
    def execute_state_action(self):

        if self.state == RobotState.PATROL:
            if self.latest_inputs.get("obstacle_detected", False):
                print("Obstacle detected during patrol. Avoiding...", flush=True)
                self.controller.avoid_obstacle()
            else:
                print("Patrolling route...", flush=True)
                self.controller.patrol()

        elif self.state == RobotState.HUMAN_DETECTED:
            print("Investigating potential human...", flush=True)
            self.controller.investigate()

        elif self.state == RobotState.CAPTURE_IMAGE:
            print("Capturing image from camera...", flush=True)
            self.controller.capture_image()

        elif self.state == RobotState.SEND_ALERT:
            print("Sending alert to monitoring system...", flush=True)
            self.controller.send_alert()

        print(f"Current State: {self.state.name}\n", flush=True)

    # ------------------------
    # Utility
    # ------------------------
    def time_in_state(self):
        return time.time() - self.state_start_time