import base64
import requests

# 🔑 Add your Hugging Face API Key here
HF_API_KEY = "Add api here"

API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

MODELS = [
    "zai-org/GLM-4.5V",
    "Qwen/Qwen2.5-VL-72B-Instruct",
    "Qwen/Qwen2.5-VL-32B-Instruct",
    "google/gemma-3-27b-it",
]


def data_url(image_bytes):
    return "data:image/jpeg;base64," + base64.b64encode(image_bytes).decode("utf-8")


def extract_err(response):
    try:
        data = response.json()
        return data.get("error", {}).get("message") or str(data)
    except:
        return response.text or "Unknown error"


def box(title, lines, icon):
    width = max(30, len(title) + 4, *(len(line) for line in lines))

    print("\n" + "┏" + "━" * (width + 2) + "┓")
    print(f"┃ {icon} {title.ljust(width - 2)} ┃")
    print("┣" + "━" * (width + 2) + "┫")

    for line in lines:
        print(f"┃ {line.ljust(width)} ┃")

    print("┗" + "━" * (width + 2) + "┛\n")


def caption_single_image():
    image_source = input("🖼️ Enter image filename (default: test.jpg): ").strip() or "test.jpg"

    try:
        with open(image_source, "rb") as f:
            img = f.read()
    except Exception as e:
        box(
            "File Error",
            [f"Could not load: {image_source}", f"Reason: {e}"],
            "❌"
        )
        return

    base_payload = {
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "Give a short caption for this image."},
                {"type": "image_url", "image_url": {"url": data_url(img)}}
            ]
        }],
        "max_tokens": 60,
        "temperature": 0.2
    }

    last_error = None

    for model in MODELS:
        payload = dict(base_payload, model=model)

        try:
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json=payload,
                timeout=120
            )
        except requests.RequestException as e:
            last_error = str(e)
            continue

        if response.status_code != 200:
            last_error = extract_err(response)
            continue

        try:
            data = response.json()
        except:
            last_error = "Invalid JSON response"
            continue

        caption = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )

        if caption:
            box(
                "Image Caption Generated",
                [
                    f"🖼️ Image  : {image_source}",
                    "📝 Caption:",
                    f"   {caption}"
                ],
                "🎉"
            )
            return

        last_error = "No caption found"

    box(
        "Caption Failed",
        [
            f"🖼️ Image  : {image_source}",
            f"❌ Error : {last_error or 'Unknown error'}"
        ],
        "⚠️"
    )


def main():
    if HF_API_KEY == "your_huggingface_api_key_here":
        print("⚠️ Please add your Hugging Face API key first!")
        return

    caption_single_image()


if __name__ == "__main__":
    main()