"""
Simple Text-to-Image Generator
Primary model first, automatic fallback if failed

INSTALL:
pip install huggingface-hub pillow
"""

from huggingface_hub import InferenceClient
from datetime import datetime

# Paste your Hugging Face API key here
HF_API_KEY = "add api key here"

# Model priority (tries in order)
MODELS = [
    "ByteDance/SDXL-Lightning",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "stabilityai/sdxl-turbo",
    "runwayml/stable-diffusion-v1-5"
]

# Create client
client = InferenceClient(api_key=HF_API_KEY)

print(f"Using primary model: {MODELS[0]}")
print("Type 'quit' to exit\n")

while True:
    prompt = input("Enter prompt: ").strip()

    if prompt.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break

    if not prompt:
        continue

    print("Generating image...")
    image = None

    # Try models one by one
    for model in MODELS:
        try:
            print(f"Trying: {model}")
            image = client.text_to_image(prompt, model=model)
            print(f"Success with: {model}")
            break
        except Exception:
            print("Failed, switching model...")

    if image:
        filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image.save(filename)
        print(f"Image saved as: {filename}")
        image.show()
    else:
        print("All models failed. Check API key or internet.\n")