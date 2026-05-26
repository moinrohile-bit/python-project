import cv2
import mediapipe as mp
import pyautogui

# Disable PyAutoGUI fail-safe pause to make scrolling smoother
pyautogui.PAUSE = 0.001

def main():
    # Initialize MediaPipe Hand tracking structures
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    mp_draw = mp.solutions.drawing_utils

    # Launch Mac webcam stream (0 is the default FaceTime HD camera)
    cap = cv2.VideoCapture(0)
    
    print("🚀 Gesture Scrolling Controller Started!")
    print("\n👋 HOW TO SCROLL YOUR MAC:")
    print("-------------------------------------------------")
    print("✋ OPEN PALM: Scroll UP")
    print("✊ CLOSED FIST: Scroll DOWN")
    print("❌ QUIT APP: Press [q] inside the video window.")
    print("-------------------------------------------------\n")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame from webcam.")
            break

        # Flip horizontally for a natural mirror mapping view
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        
        # MediaPipe requires RGB images
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        gesture_status = "No Hand Detected"
        text_color = (255, 255, 255)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw the wireframe hand skeleton overlay
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Extract landmark coordinates list
                landmarks = hand_landmarks.landmark
                
                # Check finger extension state by comparing Tip Y coordinate to MCP/PIP Y coordinate
                # In MediaPipe, Y increases downwards from the top of the frame.
                # Finger is extended if Tip Y < MCP/PIP Y (higher on screen)
                fingers_extended = [
                    landmarks[8].y < landmarks[6].y,   # Index Finger
                    landmarks[12].y < landmarks[10].y, # Middle Finger
                    landmarks[16].y < landmarks[14].y, # Ring Finger
                    landmarks[20].y < landmarks[18].y  # Pinky Finger
                ]
                
                extended_count = sum(fingers_extended)

                # 3. Classify gestures and control system actions via PyAutoGUI
                if extended_count >= 3:
                    gesture_status = "✋ Open Palm - Scrolling UP"
                    text_color = (0, 255, 0)  # Green
                    # Positive values scroll up on macOS
                    pyautogui.scroll(6)
                    
                elif extended_count <= 1:
                    gesture_status = "✊ Closed Fist - Scrolling DOWN"
                    text_color = (0, 0, 255)  # Red
                    # Negative values scroll down on macOS
                    pyautogui.scroll(-6)
                    
                else:
                    gesture_status = "😐 Neutral Hand - No Scroll"
                    text_color = (255, 255, 0)  # Yellow

        # 4. Provide real-time UI text feedback on screen layout
        cv2.rectangle(frame, (10, 10), (480, 55), (0, 0, 0), -1) # Dark background box for readability
        cv2.putText(frame, gesture_status, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2, cv2.LINE_AA)

        # Display output feed window
        cv2.imshow("Mac Hand Gesture Scrolling Engine", frame)

        # Handle keyboard quitting key bind
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources safely
    cap.release()
    cv2.destroyAllWindows()
    print("\n👋 App closed successfully.")

if __name__ == "__main__":
    main()
