import random
import time


class SimRobotController:
    def __init__(self):
        self.forward_duration_sec = 4.0
        self.turn_duration_sec = 1.0
        self.patrol_segment = "forward"
        self.segment_start_time = time.time()

    def reset_patrol_timing(self):
        self.patrol_segment = "forward"
        self.segment_start_time = time.time()
        print("SIM: patrol timing reset", flush=True)

    def patrol(self):
        now = time.time()
        elapsed = now - self.segment_start_time

        print(f"SIM: segment={self.patrol_segment} elapsed={elapsed:.2f}", flush=True)

        if self.patrol_segment == "forward":
            print("SIM: moving forward", flush=True)
            if elapsed >= self.forward_duration_sec:
                self.patrol_segment = "turn"
                self.segment_start_time = now
        else:
            print("SIM: turning", flush=True)
            if elapsed >= self.turn_duration_sec:
                self.patrol_segment = "forward"
                self.segment_start_time = now

    def avoid_obstacle(self, obstacle_side=None):
        if obstacle_side == "left":
            turn_dir = "right"
        elif obstacle_side == "right":
            turn_dir = "left"
        else:
            turn_dir = random.choice(["left", "right"])

        print(
            f"SIM: obstacle on {obstacle_side}, would turn {turn_dir}",
            flush=True,
        )
        self.reset_patrol_timing()

    def investigate(self):
        print("SIM: investigating potential human", flush=True)

    def capture_image(self):
        print("SIM: capturing image", flush=True)

    def send_alert(self):
        print("SIM: sending alert", flush=True)

    def stop(self):
        print("SIM: stop", flush=True)
