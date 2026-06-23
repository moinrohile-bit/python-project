import requests
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Paste your Hugging Face API key here
HF_API_KEY = "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"

# Default model
DEFAULT_MODEL = "facebook/bart-large-cnn"


def build_api_url(model_name):
    return f"https://api-inference.huggingface.co/models/{model_name}"


def query(payload, model_name=DEFAULT_MODEL):
    api_url = build_api_url(model_name)
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    try:
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code != 200:
            print(Fore.RED + f"❌ Error {response.status_code}: {response.text}")
            return None

        return response.json()

    except Exception as e:
        print(Fore.RED + f"❌ Request failed: {e}")
        return None


def summarize_text(text, min_length, max_length, model_name=DEFAULT_MODEL):
    payload = {
        "inputs": text,
        "parameters": {
            "min_length": min_length,
            "max_length": max_length
        }
    }

    print(Fore.BLUE + Style.BRIGHT + f"\n🚀 Summarizing using: {model_name}")

    result = query(payload, model_name)

    if result and isinstance(result, list) and "summary_text" in result[0]:
        return result[0]["summary_text"]
    else:
        print(Fore.RED + "❌ Invalid response:", result)
        return None


if __name__ == "__main__":
    print(Fore.YELLOW + Style.BRIGHT + "👋 Welcome to AI Text Summarizer")

    user_name = input("Enter your name: ").strip()
    if not user_name:
        user_name = "User"

    print(Fore.GREEN + f"Hello {user_name}! ✨")

    user_text = input("\nEnter text to summarize:\n> ").strip()

    if not user_text:
        print(Fore.RED + "❌ No text entered.")
        exit()

    print("\nChoose summary style:")
    print("1. Short Summary")
    print("2. Detailed Summary")

    choice = input("Enter choice (1/2): ").strip()

    if choice == "2":
        min_length = 80
        max_length = 200
    else:
        min_length = 30
        max_length = 100

    summary = summarize_text(user_text, min_length, max_length)

    if summary:
        print(Fore.GREEN + Style.BRIGHT + f"\n📄 Summary for {user_name}:")
        print(Fore.CYAN + summary)
    else:
        print(Fore.RED + "❌ Failed to generate summary.")