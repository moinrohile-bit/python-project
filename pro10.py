import os
import cv2
import numpy as np

# Global variables for tracking app state
WINDOW_NAME = "Interactive Edge & Filter Studio"

def nothing(x):
    pass

def run_interactive_app(image_path):
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found.")
        return

    # Load original image
    src_img = cv2.imread(image_path)
    
    # Create the interactive control window
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
    
    # ----------------------------------------------------
    # Create Trackbars for Real-Time Parameter Adjustment
    # ----------------------------------------------------
    # 1. Filter selection trackbar (0: None, 1: Gaussian, 2: Median)
    cv2.createTrackbar("Filter", WINDOW_NAME, 0, 2, nothing)
    
    # 2. Kernel size trackbar (Used for blurs) -> maps to odd numbers dynamically
    cv2.createTrackbar("Kernel Size", WINDOW_NAME, 1, 15, nothing)
    
    # 3. Edge Mode selection trackbar (0: Canny, 1: Laplacian, 2: Sobel)
    cv2.createTrackbar("Edge Mode", WINDOW_NAME, 0, 2, nothing)
    
    # 4. Canny thresholds (Only active when Canny mode is selected)
    cv2.createTrackbar("Thresh 1", WINDOW_NAME, 50, 255, nothing)
    cv2.createTrackbar("Thresh 2", WINDOW_NAME, 150, 255, nothing)

    print("🚀 Application launched successfully!")
    print("👉 Adjust the sliders on the window to change parameters in real-time.")
    print("⌨️  Press 'q' or 'ESC' inside the image window to close the application.")

    while True:
        # Read current trackbar positions
        filter_type = cv2.getTrackbarPos("Filter", WINDOW_NAME)
        k_size_idx = cv2.getTrackbarPos("Kernel Size", WINDOW_NAME)
        edge_mode = cv2.getTrackbarPos("Edge Mode", WINDOW_NAME)
        t1 = cv2.getTrackbarPos("Thresh 1", WINDOW_NAME)
        t2 = cv2.getTrackbarPos("Thresh 2", WINDOW_NAME)

        # Convert kernel index to a valid odd number (min 1, max 31)
        k_size = (k_size_idx * 2) + 1

        # Work on a copy of the original image
        processed_img = src_img.copy()

        # Step 1: Convert to Grayscale for Edge Processing
        gray = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)

        # Step 2: Apply Selected Real-time Filter
        if filter_type == 1:    # Gaussian Blur
            gray = cv2.GaussianBlur(gray, (k_size, k_size), 0)
        elif filter_type == 2:  # Median Blur
            gray = cv2.medianBlur(gray, k_size)

        # Step 3: Apply Selected Edge Detection Technique
        if edge_mode == 0:      # Canny Edge Detection
            output_display = cv2.Canny(gray, t1, t2)
        elif edge_mode == 1:    # Laplacian Edge Detection
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            output_display = cv2.convertScaleAbs(laplacian)
        else:                   # Sobel Edge Detection (Combined X and Y)
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            combined_sobel = cv2.bitwise_or(cv2.convertScaleAbs(sobelx), cv2.convertScaleAbs(sobely))
            output_display = combined_sobel

        # Display the output view
        cv2.imshow(WINDOW_NAME, output_display)

        # Handle exiting via key presses ('q' or ESC)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    sample_image = "filter_input.jpg"
    
    # Auto-generate a high-contrast test pattern if no file is present
    if not os.path.exists(sample_image):
        dummy = np.zeros((500, 700, 3), dtype=np.uint8)
        # Draw explicit geometric shapes to see sharp edges easily
        cv2.rectangle(dummy, (50, 50), (300, 450), (255, 255, 255), -1)
        cv2.circle(dummy, (500, 250), 120, (255, 255, 255), -1)
        cv2.line(dummy, (0, 0), (700, 500), (255, 255, 255), 5)
        cv2.imwrite(sample_image, dummy)
        print(f"💡 Generated a high-contrast shapes canvas named '{sample_image}' for immediate testing.")

    run_interactive_app(sample_image)
