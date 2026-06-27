import requests

# ---------------------------------------
# Paste your Hugging Face API Token here
# Example: hf_xxxxxxxxxxxxxxxxxxxxxxxxx
# ---------------------------------------
API_TOKEN = "YOUR_HUGGING_FACE_API_TOKEN"

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}


def generate_image(prompt, style, negative_prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "negative_prompt": negative_prompt,
            "style": style
        }
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            print("\nError:", response.status_code)
            print(response.text)
            return

        filename = "generated_image.png"

        with open(filename, "wb") as image_file:
            image_file.write(response.content)

        print("\nImage generated successfully!")
        print(f"Saved as: {filename}")

    except requests.exceptions.RequestException as e:
        print("Connection Error:", e)


def main():
    print("=" * 50)
    print(" Hugging Face Text-to-Image Generator ")
    print("=" * 50)

    while True:
        prompt = input("\nEnter image prompt: ")

        style = input(
            "Enter style (realistic, anime, digital art, watercolor, sketch): "
        )

        negative = input(
            "Enter negative prompt (optional): "
        )

        generate_image(prompt, style, negative)

        again = input("\nGenerate another image? (yes/no): ").lower()

        if again not in ["yes", "y"]:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()