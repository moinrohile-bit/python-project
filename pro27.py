import os
import requests

# Hugging Face model
API_URL = "add api key here"

# Read API token from environment variable
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    print("Error: HF_TOKEN environment variable is not set.")
    print("Run:")
    print('export HF_TOKEN="your_huggingface_api_token"')
    exit()

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

VALID_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)


def generate_caption(image_path):
    """Send image to Hugging Face API and return caption."""
    try:
        with open(image_path, "rb") as image_file:
            response = requests.post(
                API_URL,
                headers=HEADERS,
                data=image_file.read(),
                timeout=60
            )

        if response.status_code != 200:
            return f"API Error ({response.status_code})"

        result = response.json()

        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "No caption returned")

        if isinstance(result, dict) and "error" in result:
            return f"Error: {result['error']}"

        return "No caption generated."

    except Exception as e:
        return f"Exception: {e}"


def main():

    folder = input("Enter image folder path (press Enter for 'images'): ").strip()

    if folder == "":
        folder = "images"

    if not os.path.exists(folder):
        print(f"Folder '{folder}' does not exist.")
        return

    image_files = [
        file for file in os.listdir(folder)
        if file.lower().endswith(VALID_EXTENSIONS)
    ]

    if not image_files:
        print("No valid images found in the folder.")
        return

    show = input("Print captions while processing? (y/n): ").strip().lower()
    print_output = show == "y"

    summary_file = "captions_summary.txt"

    with open(summary_file, "w", encoding="utf-8") as output:

        output.write("Image Caption Summary\n")
        output.write("=" * 60 + "\n\n")

        for image_name in image_files:

            image_path = os.path.join(folder, image_name)

            caption = generate_caption(image_path)

            output.write(f"Image : {image_name}\n")
            output.write(f"Caption: {caption}\n")
            output.write("-" * 60 + "\n")

            if print_output:
                print(f"{image_name} -> {caption}")

    print(f"\nDone!")
    print(f"Captions saved to '{summary_file}'.")


if __name__ == "__main__":
    main()