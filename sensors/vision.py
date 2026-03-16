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
# Evidence folder
# -----------------------------
EVIDENCE_DIR = "evidence"
os.makedirs(EVIDENCE_DIR, exist_ok=True)


# -----------------------------
# Detection state tracking
# -----------------------------
person_present = False

# Only these COCO labels count as visual obstacles.
OBSTACLE_CLASSES = {
    "person",
    "chair",
    "couch",
    "bench",
    "table",
    "tv",
    "bed",
    "refrigerator",
}


def detect_person(frame):

    global person_present

    if frame is None:
        print("⚠️ No frame received")
        return False, False, None


    # -----------------------------
    # Convert CUDA → numpy
    # -----------------------------
    frame_np = jetson_utils.cudaToNumpy(frame)


    # -----------------------------
    # Fix camera orientation
    # -----------------------------
    frame_np = cv2.rotate(frame_np, cv2.ROTATE_180)
    frame_height = frame_np.shape[0]
    frame_width = frame_np.shape[1]


    # -----------------------------
    # Convert numpy → CUDA
    # -----------------------------
    img = jetson_utils.cudaFromNumpy(frame_np)


    # -----------------------------
    # Run detection
    # -----------------------------
    detections = net.Detect(img, overlay="box,labels,conf")

    print(f"Detections found: {len(detections)}")

    person_detected = False
    obstacle_detected = False
    obstacle_side = None


    for detection in detections:

        class_name = net.GetClassDesc(detection.ClassID)
        confidence = detection.Confidence

        is_obstacle_class = class_name.lower() in OBSTACLE_CLASSES
        if (
            is_obstacle_class
            and confidence > 0.6
            and detection.Bottom > frame_height * 0.55
        ):
            if not obstacle_detected:
                print("Vision obstacle detected", flush=True)
            obstacle_detected = True
            if detection.Center[0] < frame_width / 2:
                obstacle_side = "left"
            else:
                obstacle_side = "right"

        # Log everything the model sees (very helpful for debugging)
        print(f"Detected: {class_name} ({confidence:.2f})")

        # -----------------------------
        # Ignore non-person objects
        # -----------------------------
        if class_name != "person":
            continue


        # -----------------------------
        # HUMAN DETECTION
        # -----------------------------
        if confidence > 0.5:

            person_detected = True

            # Only trigger alert when a new person appears
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
    # Reset when person leaves
    # -----------------------------
    if not person_detected and person_present:
        print("👤 Person left frame")
        person_present = False


    return person_detected, obstacle_detected, obstacle_side


    return person_detected, obstacle_detected, obstacle_side