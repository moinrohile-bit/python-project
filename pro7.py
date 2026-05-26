import os
import cv2

def resize_and_save_social_media(image_path):
    # 1. Load the original image
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found.")
        print("Please place an image in the same folder or provide a valid path.")
        return

    # cv2.imread loads the image into a numpy array
    img = cv2.imread(image_path)
    
    # 2. Define the target sizes (Width, Height) for 3 common platforms
    sizes = {
        "instagram_square": (1080, 1080),
        "youtube_landscape": (1280, 720),
        "tiktok_portrait": (1080, 1920)
    }
    
    print(f"✨ Original Image Loaded Successfully. Dimensions: {img.shape[1]}x{img.shape[0]}")
    print("🔄 Resizing images...")

    # Loop through each target size configuration
    for platform, (width, height) in sizes.items():
        # 3. Resize the image using bilinear interpolation (optimal for general resizing)
        resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)
        
        # 4. Save the processed image
        output_filename = f"resized_{platform}.jpg"
        cv2.imwrite(output_filename, resized_img)
        print(f"💾 Saved: {output_filename} ({width}x{height})")
        
        # 5. Display the processed image
        # Note: Large dimensions might overflow your Mac screen, so we downscale the window view
        window_name = f"Preview - {platform.replace('_', ' ').title()}"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 400, int(400 * (height / width)))
        cv2.imshow(window_name, resized_img)
        
    print("\n🖥️  Previews are open on your screen. Press ANY KEY in any preview window to close them and exit.")
    
    # Keeps windows open on macOS until a physical keyboard key is pressed
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Change 'input.jpg' to the filename of any image file you have on your Mac
    sample_image = "input.jpg"
    
    # Create a dummy image automatically if you don't have one to test immediately
    if not os.path.exists(sample_image):
        import numpy as np
        # Create a basic 800x600 colorful placeholder image
        dummy_img = np.zeros((600, 800, 3), dtype=np.uint8)
        cv2.putText(dummy_img, "Test Photo", (250, 320), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        cv2.imwrite(sample_image, dummy_img)
        print(f"💡 Generated a placeholder image named '{sample_image}' for testing.")

    resize_and_save_social_media(sample_image)
