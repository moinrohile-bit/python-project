import os
import cv2
import numpy as np

def apply_sepia(img):
    """Applies a warm sepia filter matrix to the image."""
    sepia_matrix = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    return cv2.transform(img, sepia_matrix)

def main(image_path):
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found.")
        return

    # Load original image (OpenCV uses BGR format natively)
    original_img = cv2.imread(image_path)
    
    # Channel multipliers
    r_mult, g_mult, b_mult = 1.0, 1.0, 1.0
    
    # Filter selection state
    filters = ["None", "Grayscale", "Sepia", "Invert"]
    current_filter_idx = 0

    window_name = "Interactive Color Studio"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    print("🚀 Application launched successfully!")
    print("\n⌨️  KEYBOARD CONTROLS:")
    print("-----------------------------------------------")
    print("🔴 RED Channel:   [r] Increase | [R] Decrease")
    print("🟢 GREEN Channel: [g] Increase | [G] Decrease")
    print("🔵 BLUE Channel:  [b] Increase | [B] Decrease")
    print("🎬 COLOR FILTER:  [f] Cycle Filters (None -> Gray -> Sepia -> Invert)")
    print("💾 SAVE IMAGE:   [s] Save with custom filename")
    print("❌ QUIT APP:     [q] or [ESC]")
    print("-----------------------------------------------")

    while True:
        # 1. Start with a fresh base from the selection mode
        current_filter = filters[current_filter_idx]
        
        if current_filter == "Grayscale":
            gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
            processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        elif current_filter == "Sepia":
            processed = apply_sepia(original_img)
        elif current_filter == "Invert":
            processed = cv2.bitwise_not(original_img)
        else:
            processed = original_img.copy()

        # 2. Split channels to apply real-time RGB adjustments
        # Remember OpenCV channels layout order: Blue, Green, Red
        b_channel, g_channel, r_channel = cv2.split(processed)

        # Apply multiplier and clip boundaries safely between 0-255 scaling
        r_channel = np.clip(r_channel * r_mult, 0, 255).astype(np.uint8)
        g_channel = np.clip(g_channel * g_mult, 0, 255).astype(np.uint8)
        b_channel = np.clip(b_channel * b_mult, 0, 255).astype(np.uint8)

        # Merge channels back together
        final_display = cv2.merge([b_channel, g_channel, r_channel])

        # 3. Add information HUD onto the screen matrix
        hud_text = f"R:{r_mult:.1f} | G:{g_mult:.1f} | B:{b_mult:.1f} | Filter: {current_filter}"
        cv2.putText(final_display, hud_text, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
        
        # Display window
        cv2.imshow(window_name, final_display)

        # 4. Listen for keyboard inputs
        key = cv2.waitKey(1)
        
        if key == -1:
            continue
            
        # Exit rules
        if key == ord('q') or key == 27:
            print("\nExiting application. Goodbye!")
            break

        # Red adjustments (r / R)
        elif key == ord('r'):
            r_mult = min(r_mult + 0.1, 3.0)
        elif key == ord('R'):
            r_mult = max(r_mult - 0.1, 0.0)

        # Green adjustments (g / G)
        elif key == ord('g'):
            g_mult = min(g_mult + 0.1, 3.0)
        elif key == ord('G'):
            g_mult = max(g_mult - 0.1, 0.0)

        # Blue adjustments (b / B)
        elif key == ord('b'):
            b_mult = min(b_mult + 0.1, 3.0)
        elif key == ord('B'):
            b_mult = max(b_mult - 0.1, 0.0)

        # Cycle filters (f)
        elif key == ord('f'):
            current_filter_idx = (current_filter_idx + 1) % len(filters)
            print(f"🔄 Switched filter mode to: {filters[current_filter_idx]}")

        # Save Image (s)
        elif key == ord('s'):
            print("\n💾 Save Mode Activated!")
            filename = input("Enter custom filename to save (e.g., my_edit.jpg): ").strip()
            if filename:
                # Add file extension automatic fallback if missing
                if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    filename += '.jpg'
                
                # Save without the informational text HUD string overlay
                clean_output = cv2.merge([b_channel, g_channel, r_channel])
                cv2.imwrite(filename, clean_output)
                print(f"✨ Successfully saved your image as: {filename}\n")
            else:
                print("❌ Invalid filename. Save canceled.")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    sample_img_path = "color_studio_input.jpg"
    
    # Auto-generate a beautiful colorful sunset test profile if no image exists
    if not os.path.exists(sample_img_path):
        dummy = np.zeros((500, 700, 3), dtype=np.uint8)
        for y in range(500):
            # Create a vertical color gradient matrix shift
            dummy[y, :, 0] = int(y / 500 * 50)   # Blue
            dummy[y, :, 1] = int(y / 500 * 120)  # Green
            dummy[y, :, 2] = 200                  # Red
        cv2.circle(dummy, (350, 350), 90, (100, 230, 255), -1)
        cv2.imwrite(sample_img_path, dummy)
        print(f"💡 Generated a colorful test landscape profile named '{sample_img_path}'.")

    main(sample_img_path)
