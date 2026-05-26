import cv2
from fer import FER

def main():
    # Initialize the FER emotion detector 
    # mtcnn=False uses Haar Cascades, which run much faster for live video on Mac
    detector = FER(mtcnn=False)

    # Initialize the Mac webcam (0 is the default FaceTime HD camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Error: Could not access the webcam.")
        print("💡 Hint: Go to System Settings > Privacy & Security > Camera and ensure Terminal/VS Code is allowed.")
        return

    print("🚀 Real-Time Emotion Detector Started!")
    print("⌨️  Press the 'q' key on your keyboard while inside the video window to quit.")

    while True:
        # Capture frame-by-frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        # Detect faces and analyze emotions in the current frame
        analysis = detector.detect_emotions(frame)

        # Loop through every detected face
        for face in analysis:
            # Extract bounding box coordinates
            x, y, w, h = face["box"]
            emotions = face["emotions"]
            
            # Find the emotion with the highest confidence score
            dominant_emotion = max(emotions, key=emotions.get)
            confidence = emotions[dominant_emotion]

            # Draw a bounding box around the detected face
            # BGR Color format: (0, 255, 0) is Bright Green
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Create the text overlay string
            label = f"{dominant_emotion.capitalize()} ({int(confidence * 100)}%)"
            
            # Write the emotion label right above the face bounding box
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the live annotated camera stream
        cv2.imshow("Mac WebCam - Real-Time Emotion Analysis", frame)

        # Stop the loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up and release system hardware resources safely
    cap.release()
    cv2.destroyAllWindows()
    print("\n👋 App closed successfully.")

if __name__ == "__main__":
    main()
