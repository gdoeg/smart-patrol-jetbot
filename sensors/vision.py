import jetson_inference
import jetson_utils
import time
import os
import cv2

from services.alert_service import send_alert


# -----------------------------
# Load detection model
# -----------------------------
net = jetson_inference.detectNet(
    model="/home/gabriela/jetson-inference/data/networks/SSD-Mobilenet-v2/ssd_mobilenet_v2_coco.uff",
    labels="/home/gabriela/jetson-inference/data/networks/SSD-Mobilenet-v2/ssd_coco_labels.txt",
    input_blob="Input",
    output_cvg="NMS",
    output_bbox="NMS_1",
    threshold=0.5
)


# -----------------------------
# Start CSI camera
# -----------------------------
camera = jetson_utils.videoSource("csi://0")


# -----------------------------
# Evidence folder
# -----------------------------
EVIDENCE_DIR = "evidence"
os.makedirs(EVIDENCE_DIR, exist_ok=True)


# -----------------------------
# Detection state tracking
# -----------------------------
person_present = False


def detect_person():
    global person_present

    img = camera.Capture()

    if img is None:
        print("⚠️ No frame captured")
        return False, False


    # -----------------------------
    # Convert CUDA → numpy
    # -----------------------------
    frame = jetson_utils.cudaToNumpy(img)


    # -----------------------------
    # Fix camera orientation
    # -----------------------------
    frame = cv2.rotate(frame, cv2.ROTATE_180)


    # -----------------------------
    # Convert numpy → CUDA
    # -----------------------------
    img = jetson_utils.cudaFromNumpy(frame)


    # -----------------------------
    # Run detection
    # -----------------------------
    detections = net.Detect(img, overlay="box,labels,conf")

    print(f"Detections found: {len(detections)}")

    person_detected = False
    obstacle_detected = False

    frame_height = frame.shape[0]


    for detection in detections:

        class_name = net.GetClassDesc(detection.ClassID)
        confidence = detection.Confidence

        print(f"Detected: {class_name} ({confidence:.2f})")

        # -----------------------------
        # HUMAN DETECTION
        # -----------------------------
        if class_name == "person" and confidence > 0.5:

            person_detected = True

            # -----------------------------
            # Only send alert if person just appeared
            # -----------------------------
            if not person_present:

                filename = f"{EVIDENCE_DIR}/evidence_{int(time.time())}.jpg"

                jetson_utils.saveImageRGBA(filename, img)

                print("🚨 PERSON DETECTED")
                print(f"📸 Evidence saved: {filename}")

                try:
                    send_alert(filename, confidence)
                    print("📨 Telegram alert sent")
                except Exception as e:
                    print("❌ Failed to send alert:", e)

                person_present = True


        # -----------------------------
        # OBSTACLE DETECTION
        # -----------------------------
        # If object is close to bottom of frame it is likely in front of robot
        if detection.Bottom > frame_height * 0.75 and detection.Width > 80:

            print("⚠️ Obstacle detected in path")

            obstacle_detected = True


    # -----------------------------
    # Reset when person leaves
    # -----------------------------
    if not person_detected and person_present:
        print("👤 Person left frame")
        person_present = False


    return person_detected, obstacle_detected