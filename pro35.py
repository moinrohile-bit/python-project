import os
import base64
from pathlib import Path

from openai import OpenAI
from PIL import Image, ImageEnhance, ImageFilter


# --------------------------------------------------
# GENERATE IMAGE FROM TEXT
# --------------------------------------------------

def generate_image_from_text(prompt):
    """
    Generate an AI image from a text prompt using OpenAI.
    Returns the generated image as a PIL Image.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set."
        )

    client = OpenAI(api_key=api_key)

    print("\nGenerating AI image... Please wait.")

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    # Get Base64 image data
    image_data = base64.b64decode(
        result.data[0].b64_json
    )

    # Save temporarily
    temp_file = Path("generated_original.png")

    with open(temp_file, "wb") as file:
        file.write(image_data)

    # Open with Pillow
    image = Image.open(temp_file).convert("RGB")

    return image


# --------------------------------------------------
# DAYLIGHT EDITION
# --------------------------------------------------

def create_daylight_edition(image):
    """
    Daylight Edition:
    - Brightness +30%
    - Contrast +10%
    - Gaussian blur radius 1
    """

    # Increase brightness by 30%
    daylight = ImageEnhance.Brightness(image).enhance(1.30)

    # Increase contrast by 10%
    daylight = ImageEnhance.Contrast(daylight).enhance(1.10)

    # Gaussian blur radius 1
    daylight = daylight.filter(
        ImageFilter.GaussianBlur(radius=1)
    )

    return daylight


# --------------------------------------------------
# NIGHT MOOD
# --------------------------------------------------

def create_night_mood(image):
    """
    Night Mood:
    - Contrast +40%
    - Brightness -10%
    - Gaussian blur radius 0.5
    """

    # Increase contrast by 40%
    night = ImageEnhance.Contrast(image).enhance(1.40)

    # Reduce brightness by 10%
    night = ImageEnhance.Brightness(night).enhance(0.90)

    # Gaussian blur radius 0.5
    night = night.filter(
        ImageFilter.GaussianBlur(radius=0.5)
    )

    return night


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

def main():

    print("=" * 60)
    print("        AI IMAGE GENERATOR & EDITOR")
    print("=" * 60)

    # --------------------------------------------------
    # 1. Ask user for creative prompt
    # --------------------------------------------------

    prompt = input(
        "\nEnter a creative image description:\n> "
    ).strip()

    if not prompt:
        print("Error: Prompt cannot be empty.")
        return

    # --------------------------------------------------
    # 2. Generate original AI image
    # --------------------------------------------------

    try:
        original_image = generate_image_from_text(prompt)

    except Exception as error:
        print("\nError generating image:")
        print(error)
        return

    print("AI image generated successfully.")

    # --------------------------------------------------
    # Create filename
    # --------------------------------------------------

    # Convert prompt into a safe filename
    safe_name = "".join(
        character if character.isalnum() else "_"
        for character in prompt
    )

    # Limit filename length
    safe_name = safe_name[:50].strip("_")

    if not safe_name:
        safe_name = "original_prompt"

    # --------------------------------------------------
    # 3. Create Daylight Edition
    # --------------------------------------------------

    print("\nCreating Daylight Edition...")

    daylight_image = create_daylight_edition(
        original_image
    )

    daylight_filename = (
        f"{safe_name}_daylight.png"
    )

    daylight_image.save(
        daylight_filename,
        format="PNG"
    )

    print(
        f"Saved: {daylight_filename}"
    )

    # --------------------------------------------------
    # 4. Create Night Mood
    # --------------------------------------------------

    print("\nCreating Night Mood...")

    night_image = create_night_mood(
        original_image
    )

    night_filename = (
        f"{safe_name}_night.png"
    )

    night_image.save(
        night_filename,
        format="PNG"
    )

    print(
        f"Saved: {night_filename}"
    )

    # --------------------------------------------------
    # 5. Display both images one after another
    # --------------------------------------------------

    print("\nOpening Daylight Edition...")

    daylight_image.show()

    input(
        "\nPress ENTER to display Night Mood..."
    )

    print("\nOpening Night Mood...")

    night_image.show()

    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)

    print(
        f"\nDaylight file: {daylight_filename}"
    )

    print(
        f"Night file:    {night_filename}"
    )


# --------------------------------------------------
# PROGRAM START
# --------------------------------------------------

if __name__ == "__main__":
    main()