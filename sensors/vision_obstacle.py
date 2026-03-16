import cv2
import numpy as np
import jetson_utils


def detect_obstacle(frame):

    if frame is None:
        return False

    img = jetson_utils.cudaToNumpy(frame)

    h, w, _ = img.shape

    # Focus on bottom center
    roi = img[int(h * 0.65):h, int(w * 0.25):int(w * 0.75)]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blurred, 60, 160)

    edge_density = np.count_nonzero(edges) / edges.size

    print(f"Edge density: {edge_density:.3f}")

    if edge_density > 0.08:
        print("⚠️ Visual obstacle detected")
        return True

    return False