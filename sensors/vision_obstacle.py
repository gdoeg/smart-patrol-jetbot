import cv2
import numpy as np
import jetson_utils


def detect_obstacle(video_source):

    frame = video_source.Capture()

    if frame is None:
        return False

    img = jetson_utils.cudaToNumpy(frame)

    h, w, _ = img.shape

    roi = img[int(h * 0.6):h, :]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150)

    edge_density = np.sum(edges) / edges.size

    if edge_density > 0.2:
        print("⚠️ Visual obstacle detected")
        return True

    return False