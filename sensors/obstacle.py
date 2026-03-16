import cv2
import numpy as np
import jetson_utils


def detect_obstacle(video_source):

    frame = video_source.Capture()

    if frame is None:
        return False

    img = jetson_utils.cudaToNumpy(frame)

    h, w, _ = img.shape

    # bottom region of image
    roi = img[int(h * 0.6):h, :]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    mean_intensity = np.mean(gray)

    # darker region means something is blocking view
    if mean_intensity < 60:
        return True

    return False