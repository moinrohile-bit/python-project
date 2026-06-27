import time
import requests
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO

# ==========================================
# ADD YOUR HUGGING FACE API KEY HERE
# ==========================================
HF_API_KEY = "add API here"

# Models (Primary + Fallbacks)
MODELS = [
    "black-forest-labs/FLUX.1-schnell",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "runwayml/stable-diffusion-v1-5",
    "CompVis/stable-diffusion-v1-4",
]

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Accept": "image/png"
}


def generate_image_from_text(prompt):
    """
    Generate image from text using Hugging Face API
    """
    payload = {"inputs": prompt}
    last_error = None

    for model in MODELS:
        print(f"Trying model: {model}")
        url = f"https://router.huggingface.co/hf-inference/models/{model}"

        for attempt in range(3):
            try:
                response = requests.post(
                    url,
                    headers=HEADERS,
                    json=payload,
                    timeout=120
                )

                content_type = response.headers.get("content-type", "").lower()

                # Model loading (503)
                if response.status_code == 503 and "application/json" in content_type:
                    wait_time = response.json().get("estimated_time", 5)
                    print(f"Model loading... waiting {wait_time}s")
                    time.sleep(wait_time + 1)
                    continue

                # Success
                if response.status_code == 200 and "image" in content_type:
                    return Image.open(BytesIO(response.content)).convert("RGB")

                # Error response
                try:
                    error_data = response.json()
                except:
                    error_data = response.text

                last_error = f"Error {response.status_code}: {error_data}"
                break

            except Exception as e:
                last_error = str(e)

    raise Exception(last_error or "Unknown error")


def post_process_image(image):
    """
    Apply simple enhancements
    """
    image = ImageEnhance.Brightness(image).enhance(1.2)
    image = ImageEnhance.Contrast(image).enhance(1.3)
    image = image.filter(ImageFilter.GaussianBlur(radius=1))
    return image


def main():
    print("=" * 50)
    print("AI Text-to-Image Generator")
    print("Type 'exit' anytime to quit")
    print("=" * 50)

    while True:
        prompt = input("\nEnter image prompt: ")

        if prompt.lower() == "exit":
            print("Goodbye!")
            break

        try:
            print("\nGenerating image...")
            image = generate_image_from_text(prompt)

            print("Applying enhancements...")
            final_image = post_process_image(image)

            # Show image
            final_image.show()

            # Save option
            save = input("\nSave image? (yes/no): ").strip().lower()
            if save == "yes":
                filename = input("Enter filename: ").strip()
                final_image.save(f"{filename}.png")
                print(f"Saved as {filename}.png")

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()