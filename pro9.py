import os
import cv2
import numpy as np

def annotate_image_width(image_path):
    # 1. Load the target image
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found.")
        return

    img = cv2.imread(image_path)
    height, width, _ = img.shape
    print(f"📐 Image Loaded. Dimensions: {width}x{height}")

    # 2. Dynamically calculate layout positions
    # Position the arrow line horizontally in the middle of the image
    padding = 40  # Keep arrow slightly inside the margins
    start_point = (padding, height // 2)
    end_point = (width - padding, height // 2)
    
    color = (0, 255, 0)      # Bright Green (BGR format)
    thickness = 3
    tip_length = 0.05        # Length of arrow head relative to line length

    # 3. Draw Bi-directional Arrow using cv2.arrowedLine()
    # Left-to-Right arrow
    cv2.arrowedLine(img, start_point, end_point, color, thickness, tipLength=tip_length)
    # Right-to-Left arrow
    cv2.arrowedLine(img, end_point, start_point, color, thickness, tipLength=tip_length)

    # 4. Add dynamic text overlay using cv2.putText()
    text = f"Width: {width} px"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.0
    text_thickness = 2
    
    # Calculate text size to perfectly center it horizontally above the arrow
    text_size = cv2.getTextSize(text, font, font_scale, text_thickness)[0]
    text_x = (width - text_size[0]) // 2
    text_y = (height // 2) - 15  # 15 pixels offset above the arrow line

    cv2.putText(img, text, (text_x, text_y), font, font_scale, color, text_thickness, cv2.LINE_AA)

    # 5. Save and Display result
    output_filename = "annotated_width.jpg"
    cv2.imwrite(output_filename, img)
    print(f"💾 Saved annotated image to: {output_filename}")

    # Display using a standard scalable preview window
    window_name = "Width Measurement Annotation"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, img)
    
    print("\n🖥️  Preview window opened. Press ANY KEY in the window to close and exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    sample_image = "measurement_input.jpg"
    
    # Auto-generate a clean dark gray image canvas if no file exists to test immediately
    if not os.path.exists(sample_image):
        dummy_canvas = np.ones((600, 800, 3), dtype=np.uint8) * 50
        cv2.imwrite(sample_image, dummy_canvas)
        print(f"💡 Generated a blank 800x600 test canvas named '{sample_image}'.")

    annotate_image_width(sample_image)
