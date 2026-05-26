import os
import cv2
import numpy as np

def process_gallery_image(image_path):
    # 0. Load the image
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found.")
        print("Please place a test image in the same folder or update the file path.")
        return

    # Load image natively in BGR format
    img = cv2.imread(image_path)
    height, width, _ = img.shape
    print(f"🖼️  Successfully loaded original image. Dimensions: {width}x{height}")

    # 1. Rotate the image to realign it
    # Options: cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_180, cv2.ROTATE_90_COUNTERCLOCKWISE
    rotated_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    print("🔄 Step 1 complete: Image rotated 90 degrees clockwise.")

    # 2. Adjust brightness for a vibrant look
    # Using cv2.convertScaleAbs: output = input * alpha + beta
    # beta increases brightness; alpha adjusts contrast
    bright_img = cv2.convertScaleAbs(img, alpha=1.1, beta=45)
    print("☀️ Step 2 complete: Brightness and vibrancy boosted.")

    # 3. Crop the image to highlight the main subject
    # Example: Slicing the inner 50% section from the center of the image
    start_y = int(height * 0.25)
    end_y = int(height * 0.75)
    start_x = int(width * 0.25)
    end_x = int(width * 0.75)
    
    cropped_img = img[start_y:end_y, start_x:end_x]
    print(f"✂️  Step 3 complete: Cropped center region down to {end_x - start_x}x{end_y - start_y}.")

    # 4. Save the processed gallery assets
    cv2.imwrite("gallery_rotated.jpg", rotated_img)
    cv2.imwrite("gallery_brightened.jpg", bright_img)
    cv2.imwrite("gallery_cropped.jpg", cropped_img)
    print("\n💾 All transformed portfolio files successfully exported to disk!")

    # 5. Interactively display the transformed results on your screen
    cv2.imshow("Original Gallery Image", img)
    cv2.imshow("1. Rotated Asset", rotated_img)
    cv2.imshow("2. Brightened Asset", bright_img)
    cv2.imshow("3. Cropped Subject Focus", cropped_img)

    print("\n🖥️  Display windows opened. Press ANY KEY while focused on a window to close and exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    sample_file = "gallery_input.jpg"
    
    # Auto-generate a grid-based placeholder image if no testing image exists yet
    if not os.path.exists(sample_file):
        dummy_canvas = np.zeros((600, 600, 3), dtype=np.uint8)
        # Construct contrasting geometrical targets
        cv2.rectangle(dummy_canvas, (100, 100), (500, 500), (255, 120, 0), -1)
        cv2.circle(dummy_canvas, (300, 300), 120, (0, 255, 255), -1)
        cv2.putText(dummy_canvas, "GALLERY TOP", (160, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
        cv2.imwrite(sample_file, dummy_canvas)
        print(f"💡 Generated an initial testing template file named '{sample_file}'.")

    process_gallery_image(sample_file)
