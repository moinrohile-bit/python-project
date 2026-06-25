import cv2
import mediapipe as mp
import numpy as np
import math
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# Open Webcam
cap = cv2.VideoCapture(0)

current_filter = "Normal"
last_action_time = 0
cooldown = 1.0  # seconds

# ---------- Filter Functions ----------

def apply_grayscale(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

def apply_sepia(frame):
    kernel = np.array([
        [0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.393, 0.769, 0.189]
    ])
    sepia = cv2.transform(frame, kernel)
    return np.clip(sepia, 0, 255).astype(np.uint8)

def apply_negative(frame):
    return cv2.bitwise_not(frame)

# ---------- Distance Function ----------

def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

print("Gesture Controls:")
print("Thumb + Index  -> Capture Photo")
print("Thumb + Middle -> Grayscale")
print("Thumb + Ring   -> Sepia")
print("Thumb + Pinky  -> Negative")
print("Press 'q' to quit")

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            lm = hand_landmarks.landmark

            thumb_tip = lm[4]
            index_tip = lm[8]
            middle_tip = lm[12]
            ring_tip = lm[16]
            pinky_tip = lm[20]

            threshold = 0.05
            current_time = time.time()

            # Thumb + Index = Capture
            if distance(thumb_tip, index_tip) < threshold:
                if current_time - last_action_time > cooldown:
                    filename = f"capture_{int(time.time())}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"Photo saved: {filename}")
                    last_action_time = current_time

            # Thumb + Middle = Grayscale
            elif distance(thumb_tip, middle_tip) < threshold:
                if current_time - last_action_time > cooldown:
                    current_filter = "Grayscale"
                    print("Filter: Grayscale")
                    last_action_time = current_time

            # Thumb + Ring = Sepia
            elif distance(thumb_tip, ring_tip) < threshold:
                if current_time - last_action_time > cooldown:
                    current_filter = "Sepia"
                    print("Filter: Sepia")
                    last_action_time = current_time

            # Thumb + Pinky = Negative
            elif distance(thumb_tip, pinky_tip) < threshold:
                if current_time - last_action_time > cooldown:
                    current_filter = "Negative"
                    print("Filter: Negative")
                    last_action_time = current_time

    # Apply selected filter
    if current_filter == "Grayscale":
        frame = apply_grayscale(frame)

    elif current_filter == "Sepia":
        frame = apply_sepia(frame)

    elif current_filter == "Negative":
        frame = apply_negative(frame)

    cv2.putText(
        frame,
        f"Filter: {current_filter}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Gesture Controlled Filters", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()