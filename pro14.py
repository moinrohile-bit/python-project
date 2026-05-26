import os
import cv2
import numpy as np

def apply_tint(img, tint_color):
    """Applies a color tint by isolates or boosting a specific channel."""
    b, g, r = cv2.split(img)
    blank = np.zeros_like(b)
    
    if tint_color == "red":
        return cv2.merge([blank, blank, r])
    elif tint_color == "green":
        return cv2.merge([blank, g, blank])
    elif tint_color == "blue":
        return cv2.merge([b, blank, blank])
    return img

def main(image_path):
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found.")
        return

    # Load base image
    original_img = cv2.imread(image_path)
    
    # State flags
    current_tint = "none"       # Options: "none", "red", "green", "blue"
    current_edge = "none"       # Options: "none", "canny", "sobel"

    window_name = "Real-Time Image Processing Studio"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    print("🚀 Real-Time Studio Activated!")
    print("\n⌨️  KEYBOARD CONTROLS:")
    print("-------------------------------------------------")
    print("🔴 Press [r] -> Apply Red Tint")
    print("🟢 Press [g] -> Apply Green Tint")
    print("🔵 Press [b] -> Apply Blue Tint")
    print("⚡ Press [c] -> Toggle Canny Edge Detection")
    print("🌀 Press [s] -> Toggle Sobel Edge Detection")
    print("🔄 Press [spacebar] -> Reset Filters & Edges")
    print("❌ Press [q] or [ESC] -> Quit Application")
    print("-------------------------------------------------")

    while True:
        # Step 1: Start with a fresh image copy and apply color tinting
        processed = apply_tint(original_img.copy(), current_tint)

        # Step 2: Extract Grayscale for edge algorithms if an edge mode is selected
        if current_edge != "none":
            gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
            
            if current_edge == "canny":
                edges = cv2.Canny(gray, 100, 200)
                # Convert back to 3 channels so text HUD displays properly
                processed = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
                
            elif current_edge == "sobel":
                sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
                sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
                abs_sobel_x = cv2.convertScaleAbs(sobel_x)
                abs_sobel_y = cv2.convertScaleAbs(sobel_y)
                edges = cv2.bitwise_or(abs_sobel_x, abs_sobel_y)
                processed = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Step 3: Draw an Information Text overlay
        hud_text = f"Tint: {current_tint.upper()} | Edge Mode: {current_edge.upper()}"
        cv2.putText(processed, hud_text, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
        
        # Display the frame
        cv2.imshow(window_name, processed)

        # Step 4: Capture keyboard input
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q') or key == 27: # Quit
            break
        elif key == ord('r'):
            current_tint = "none" if current_tint == "red" else "red"
        elif key == ord('g'):
            current_tint = "none" if current_tint == "green" else "green"
        elif key == ord('b'):
            current_tint = "none" if current_tint == "blue" else "blue"
        elif key == ord('c'):
            current_edge = "none" if current_edge == "canny" else "canny"
        elif key == ord('s'):
            current_edge = "none" if current_edge == "sobel" else "sobel"
        elif key == 32: # Spacebar
            current_tint = "none"
            current_edge = "none"

    cv2.destroyAllWindows()

if __name__ == "__main__":
    sample_file = "realtime_input.jpg"
    
    # Generate an elegant geometric test asset if no file is present
    if not os.path.exists(sample_file):
        dummy = np.zeros((500, 700, 3), dtype=np.uint8)
        cv2.rectangle(dummy, (80, 80), (320, 420), (200, 200, 200), -1)
        cv2.circle(dummy, (520, 250), 110, (150, 150, 150), -1)
        cv2.putText(dummy, "KEYBOARD LAB", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        cv2.imwrite(sample_file, dummy)
        print(f"💡 Created a sharp geometric canvas named '{sample_file}' for optimal edge testing.")

    main(sample_file)
