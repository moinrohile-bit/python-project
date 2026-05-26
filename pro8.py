import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

def manipulate_portfolio_image(image_path):
    # 0. Load the original image
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found.")
        return

    # OpenCV loads images in BGR format by default
    bgr_img = cv2.imread(image_path)
    # Convert to RGB for proper color display in Matplotlib
    orig_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    
    h, w, _ = orig_img.shape
    print(f"✨ Original Image Loaded. Dimensions: {w}x{h}")

    # 1. Rotate the image (e.g., 90 degrees clockwise)
    # You can change cv2.ROTATE_90_CLOCKWISE to ROTATE_180 or ROTATE_90_COUNTERCLOCKWISE
    rotated_img = cv2.rotate(orig_img, cv2.ROTATE_90_CLOCKWISE)
    print("🔄 Step 1: Image rotated 90 degrees.")

    # 2. Brighten the image
    # cv2.convertScaleAbs changes brightness using: output = input * alpha + beta
    # beta > 0 increases brightness (adds to pixel value)
    bright_img = cv2.convertScaleAbs(orig_img, alpha=1.0, beta=50)
    print("☀️ Step 2: Brightness boosted (+50 pixels value).")

    # 3. Crop a section of the image (Highlighting the center region as an example)
    # Slicing syntax: [startY:endY, startX:endX]
    start_y, end_y = int(h * 0.25), int(h * 0.75)
    start_x, end_x = int(w * 0.25), int(w * 0.75)
    cropped_img = orig_img[start_y:end_y, start_x:end_x]
    print(f"✂️ Step 3: Cropped center region to dimensions: {end_x-start_x}x{end_y-start_y}")

    # 4. Save the manipulated images to disk
    # Convert back to BGR before saving since cv2.imwrite expects BGR
    cv2.imwrite("portfolio_rotated.jpg", cv2.cvtColor(rotated_img, cv2.COLOR_RGB2BGR))
    cv2.imwrite("portfolio_brightened.jpg", cv2.cvtColor(bright_img, cv2.COLOR_RGB2BGR))
    cv2.imwrite("portfolio_cropped.jpg", cv2.cvtColor(cropped_img, cv2.COLOR_RGB2BGR))
    print("\n💾 All transformed versions saved successfully to your folder!")

    # 5. Visualize all steps alongside the original using Matplotlib
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.imshow(orig_img)
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(2, 2, 2)
    plt.imshow(rotated_img)
    plt.title("1. Rotated Image")
    plt.axis("off")

    plt.subplot(2, 2, 3)
    plt.imshow(bright_img)
    plt.title("2. Brightened Image")
    plt.axis("off")

    plt.subplot(2, 2, 4)
    plt.imshow(cropped_img)
    plt.title("3. Cropped Subject")
    plt.axis("off")

    plt.tight_layout()
    plt.suptitle("Photo Portfolio Transformation Pipeline", fontsize=16, y=1.02)
    plt.show()

if __name__ == "__main__":
    sample_image = "portfolio_input.jpg"
    
    # Auto-generate a grid-pattern test image if no file is present
    if not os.path.exists(sample_image):
        dummy = np.zeros((600, 600, 3), dtype=np.uint8)
        # Create a colorful pattern so rotation/cropping is obvious
        cv2.rectangle(dummy, (150, 150), (450, 450), (0, 255, 0), -1) 
        cv2.circle(dummy, (300, 300), (100), (0, 0, 255), -1)
        cv2.putText(dummy, "TOP", (260, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        cv2.imwrite(sample_image, dummy)
        print(f"💡 Generated a placeholder portfolio image named '{sample_image}' for testing.")

    manipulate_portfolio_image(sample_image)
