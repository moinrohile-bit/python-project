# old_photo_restore.py

from PIL import Image
import matplotlib.pyplot as plt
import os


def generate_inpainting_image(prompt, image_path, mask_path):
    """
    Placeholder function.
    Replace with your actual AI inpainting API call.
    Returns a PIL Image object.
    """

    print("\nGenerating restored image...")
    print(f"Prompt: {prompt}")
    print(f"Image: {image_path}")
    print(f"Mask: {mask_path}")

    # For assignment/demo purposes,
    # return the original image.
    return Image.open(image_path).convert("RGBA")


def display_image(img, title="Image"):
    plt.figure(figsize=(8, 6))
    plt.imshow(img)
    plt.title(title)
    plt.axis("off")
    plt.show()


def main():

    image_path = "old_photo.png"
    mask_path = "old_photo_mask.png"

    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found.")
        return

    if not os.path.exists(mask_path):
        print(f"Error: {mask_path} not found.")
        return

    prompt = input(
        "Enter restoration description\n"
        '(Example: "restore the torn edges and faded areas"):\n> '
    ).strip()

    if not prompt:
        prompt = "restore tears, scratches, and faded areas"

    print("\nOpening source image...")
    original = Image.open(image_path)
    display_image(original, "Original Image")

    print("Opening mask...")
    mask = Image.open(mask_path)
    display_image(mask, "Repair Mask")

    restored_image = generate_inpainting_image(
        prompt,
        image_path,
        mask_path
    )

    display_image(restored_image, "Restored Preview")

    save_choice = input(
        "\nSave restored image? (y/n): "
    ).strip().lower()

    if save_choice == "y":
        output_file = "old_photo_restored.png"
        restored_image.save(output_file)
        print(f"Saved as: {output_file}")
    else:
        print("Image not saved.")

    print("\nDone.")


if __name__ == "__main__":
    main()