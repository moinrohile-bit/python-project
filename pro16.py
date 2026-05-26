import cv2
import mediapipe as mp
import math
import os
import numpy as np
import screen_brightness_control as sbc

def set_mac_volume(volume_level):
    """Controls native macOS system volume (0 to 100)."""
    os.system(f"osascript -e 'set volume output volume {volume_level}'")

def main():
    # Initialize MediaPipe Hand tracking structures
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    # Launch Mac webcam stream
    cap = cv2.VideoCapture(0)
    
    print("🚀 Gesture Controller Active!")
    print("\n👋 HOW TO CONTROL YOUR MAC:")
    print("-------------------------------------------------")
    print("🔊 VOLUME: Pinch THUMB and INDEX finger.")
    print("☀️  BRIGHTNESS: Pinch THUMB and MIDDLE finger.")
    print("❌ QUIT APP: Press [q] inside the video window.")
    print("-------------------------------------------------\n")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip horizontally for natural mirror behavior
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame for hand landmarks
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand wireframe skeleton overlay
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Extract landmark coordinates
                landmarks = hand_landmarks.landmark
                
                # Tip points: Thumb(4), Index(8), Middle(12)
                thumb = (int(landmarks[4].x * w), int(landmarks[4].y * h))
                index = (int(landmarks[8].x * w), int(landmarks[8].y * h))
                middle = (int(landmarks[12].x * w), int(landmarks[12].y * h))

                # 1. Volume Control Logic (Thumb to Index Distance)
                vol_dist = math.hypot(index[0] - thumb[0], index[1] - thumb[1])
                # Map pixel distance (approx 20 to 150) to volume percentage (0 to 100)
                vol_level = int(np.interp(vol_dist, [20, 150], [0, 100]))
                set_mac_volume(vol_level)

                # 2. Brightness Control Logic (Thumb to Middle Distance)
                bright_dist = math.hypot(middle[0] - thumb[0], middle[1] - thumb[1])
                # Map pixel distance (approx 20 to 150) to brightness percentage (0 to 100)
                bright_level = int(np.interp(bright_dist, [20, 150], [0, 100]))
                try:
                    sbc.set_brightness(bright_level)
                except Exception:
                    pass # Prevents crashing if external display lacks DDC/CI control

                # Draw UI feedback circles on the live stream
                cv2.circle(frame, thumb, 10, (255, 0, 0), -1)
                cv2.circle(frame, index, 10, (0, 255, 0), -1)
                cv2.circle(frame, middle, 10, (0, 0, 255), -1)
                
                # Print HUD indicators on canvas screen
                cv2.putText(frame, f"Vol: {vol_level}%", (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Bright: {bright_level}%", (15, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Mac Gesture Engine Workspace", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
