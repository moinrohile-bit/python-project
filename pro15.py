import cv2
import numpy as np

def main():
    # Initialize the webcam (0 is your Mac's built-in FaceTime HD camera)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not access the webcam.")
        print("💡 Hint: Go to System Settings > Privacy & Security > Camera and ensure Terminal/VS Code is allowed.")
        return

    # Define the HSV color range for tracking an object.
    # By default, this is tuned for a bright BLUE object.
    # Tip: You can adjust these ranges to track a red, green, or yellow object instead.
    lower_color = np.array([100, 100, 100])
    upper_color = np.array([140, 255, 255])

    # Deque/list to store tracked pointer points for drawing interactive canvas actions
    drawing_points = []

    print("🚀 Real-Time Gesture Tracking Studio Started!")
    print("\n💡 HOW TO TEST GESTURES:")
    print("-------------------------------------------------")
    print("1. Hold up a bright BLUE object in front of your webcam.")
    print("2. Move it around to draw interactive lines on the screen.")
    print("-------------------------------------------------")
    print("⌨️  KEYBOARD CONTROLS:")
    print("🔄 Press [spacebar] -> Clear the drawing canvas")
    print("❌ Press [q] or [ESC] -> Quit Application")
    print("-------------------------------------------------\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        # Flip frame horizontally for a natural mirror-view mapping experience
        frame = cv2.flip(frame, 1)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 1. Apply color filtering to isolate the tracked object color
        mask = cv2.threshold(hsv_frame, lower_color, upper_color)[1]
        
        # Clean up noise using morphological operations (Erosion and Dilation)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # 2. Contour detection to locate the gesture object structure shape boundaries
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = None

        # Only proceed if at least one valid contour is detected
        if len(contours) > 0:
            # Find the largest contour matching your color footprint
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Compute minimum enclosing circle to get center point coordinates
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
            M = cv2.moments(largest_contour)
            
            # Ensure the object meets a minimum size threshold to prevent background noise triggers
            if radius > 15:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                
                # Draw a tracker boundary circle and center pinpoint dot indicator
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                
                # Track the pointer coordinate position across active frames
                drawing_points.append(center)

        # 3. Interactive Action: Draw lines connecting the saved historical points onto the screen view
        for i in range(1, len(drawing_points)):
            if drawing_points[i - 1] is None or drawing_points[i] is None:
                continue
            # Draw a thick neon trail line segment mapping the gesture flow path
            cv2.line(frame, drawing_points[i - 1], drawing_points[i], (0, 255, 0), 4)

        # Draw active mode HUD text string mapping instructions directly onto the display canvas
        cv2.putText(frame, f"Tracking Points Logged: {len(drawing_points)}", (15, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        # Display windows
        cv2.imshow("Live Gesture Controller Canvas", frame)
        cv2.imshow("Color Filter Mask Output (Debugging View)", mask)

        # Listen to keyboard input actions
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q') or key == 27:  # Exit program
            break
        elif key == 32:  # Spacebar key clears current drawing canvas arrays completely
            drawing_points.clear()
            print("🔄 Canvas cleared successfully!")

    cap.release()
    cv2.destroyAllWindows()
    print("\n👋 Application closed successfully.")

if __name__ == "__main__":
    main()
