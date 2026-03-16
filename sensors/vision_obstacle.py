import cv2
import numpy as np
import jetson_utils


def detect_obstacle(video_source):

    frame = video_source.Capture()

    if frame is None:
        return False

    img = jetson_utils.cudaToNumpy(frame)

    h, w, _ = img.shape

    # --------------------------------
    # Region of Interest (center bottom)
    # --------------------------------
    roi = img[int(h * 0.65):h, int(w * 0.25):int(w * 0.75)]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection
    edges = cv2.Canny(blurred, 60, 160)

    # Edge density calculation
    edge_density = np.sum(edges) / edges.size

    # Debug print so you can tune threshold
    print(f"Edge density: {edge_density:.3f}")

    # --------------------------------
    # Obstacle threshold
    # --------------------------------
    if edge_density > 0.35:
        print("⚠️ Visual obstacle detected")
        return True

    return False