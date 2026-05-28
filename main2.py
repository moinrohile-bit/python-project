import os
import cv2
import time
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision

# -----------------------------------
# CONFIG
# -----------------------------------
MODEL_PATH = "hand_landmarker.task"

WINDOW_NAME = "Gesture Photo App"

THRESHOLD_TOUCH = 40
PINCH_THRESHOLD = 30
DEBOUNCE = 0.8
CAPTURE_DELAY = 1.2

# -----------------------------------
# CHECK MODEL
# -----------------------------------
if not os.path.exists(MODEL_PATH):
    print("ERROR: hand_landmarker.task not found!")
    print("Run:")
    print(
        "curl -o hand_landmarker.task "
        "https://storage.googleapis.com/"
        "mediapipe-models/hand_landmarker/"
        "hand_landmarker/float16/1/"
        "hand_landmarker.task"
    )
    exit()

# -----------------------------------
# MEDIAPIPE TASKS SETUP
# -----------------------------------
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions
VisionRunningMode = vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

landmarker = HandLandmarker.create_from_options(
    options
)

# -----------------------------------
# LANDMARK IDs
# -----------------------------------
TIP_IDS = {
    "thumb": 4,
    "index": 8,
    "middle": 12,
    "ring": 16,
    "pinky": 20,
}

FILTERS = {
    "middle": ["SEPIA", "NEGATIVE"],
    "ring": ["BLUR", "GLITCH"],
    "pinky": ["EDGE", "CARTOON"]
}

filter_index = {
    "middle": 0,
    "ring": 0,
    "pinky": 0
}

current_filter = "SEPIA"

last_action = 0
last_capture = 0
pinch_active = False

SEPIA_MATRIX = np.array([
    [0.272, 0.534, 0.131],
    [0.349, 0.686, 0.168],
    [0.393, 0.769, 0.189]
])

# -----------------------------------
# FILTER FUNCTION
# -----------------------------------
def apply_filter(frame, mode):

    if mode == "SEPIA":
        return np.clip(
            cv2.transform(
                frame,
                SEPIA_MATRIX
            ),
            0,
            255
        ).astype(np.uint8)

    elif mode == "NEGATIVE":
        return cv2.bitwise_not(frame)

    elif mode == "BLUR":
        return cv2.GaussianBlur(
            frame,
            (15, 15),
            0
        )

    elif mode == "GLITCH":
        h, w = frame.shape[:2]

        r = frame[:, :, 2]
        g = frame[:, :, 1]
        b = frame[:, :, 0]

        return cv2.merge([
            np.roll(
                b,
                -int(0.03 * w),
                axis=1
            ),
            g,
            np.roll(
                r,
                int(0.04 * w),
                axis=1
            )
        ])

    elif mode == "EDGE":
        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        edges = cv2.Canny(
            gray,
            80,
            160
        )

        return cv2.cvtColor(
            edges,
            cv2.COLOR_GRAY2BGR
        )

    elif mode == "CARTOON":
        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        edges = cv2.adaptiveThreshold(
            cv2.medianBlur(gray, 7),
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            9,
            2
        )

        color = cv2.bilateralFilter(
            frame,
            9,
            75,
            75
        )

        return cv2.bitwise_and(
            color,
            color,
            mask=edges
        )

    return frame

# -----------------------------------
# CAMERA (Mac Compatible)
# -----------------------------------
cap = cv2.VideoCapture(
    0,
    cv2.CAP_AVFOUNDATION
)

if not cap.isOpened():
    print("Could not open webcam.")
    exit()

print("Camera started successfully!")

# -----------------------------------
# MAIN LOOP
# -----------------------------------
while True:

    ret, frame = cap.read()

    if not ret:
        continue

    frame = cv2.flip(frame, 1)

    h, w = frame.shape[:2]

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    timestamp = int(
        time.time() * 1000
    )

    result = landmarker.detect_for_video(
        mp_image,
        timestamp
    )

    now = time.time()

    if result.hand_landmarks:

        hand = result.hand_landmarks[0]

        points = {}

        for name, idx in TIP_IDS.items():

            x = int(
                hand[idx].x * w
            )

            y = int(
                hand[idx].y * h
            )

            points[name] = (x, y)

            cv2.circle(
                frame,
                (x, y),
                8,
                (0, 255, 0),
                -1
            )

        tx, ty = points["thumb"]
        ix, iy = points["index"]

        # PINCH TO CAPTURE
        pinch = (
            abs(tx - ix)
            < PINCH_THRESHOLD
            and
            abs(ty - iy)
            < PINCH_THRESHOLD
        )

        if (
            pinch
            and not pinch_active
            and now - last_capture
            > CAPTURE_DELAY
        ):
            pinch_active = True
            last_capture = now

            img = apply_filter(
                frame.copy(),
                current_filter
            )

            filename = (
                f"photo_"
                f"{int(now)}.jpg"
            )

            cv2.imwrite(
                filename,
                img
            )

            print(
                f"Saved: {filename}"
            )

        if not pinch:
            pinch_active = False

        # CHANGE FILTERS
        for finger in [
            "middle",
            "ring",
            "pinky"
        ]:

            fx, fy = points[finger]

            touching = (
                abs(tx - fx)
                < THRESHOLD_TOUCH
                and
                abs(ty - fy)
                < THRESHOLD_TOUCH
            )

            if (
                touching
                and now - last_action
                > DEBOUNCE
            ):
                filter_index[
                    finger
                ] ^= 1

                current_filter = (
                    FILTERS[
                        finger
                    ][
                        filter_index[
                            finger
                        ]
                    ]
                )

                print(
                    "Filter:",
                    current_filter
                )

                last_action = now

    output = apply_filter(
        frame,
        current_filter
    )

    cv2.putText(
        output,
        f"Filter: {current_filter}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        WINDOW_NAME,
        output
    )

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()