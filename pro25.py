import requests
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Replace with your Hugging Face API key
API_KEY = "YOUR_HUGGING_FACE_API_KEY"

MODELS = {
    "1": "google/pegasus-xsum",
    "2": "facebook/bart-large-cnn"
}

headers = {
    "Authorization": f"Bearer {API_KEY}"
}


def summarize(text, model, min_len, max_len):
    url = f"https://api-inference.huggingface.co/models/{model}"

    payload = {
        "inputs": text,
        "parameters": {
            "min_length": min_len,
            "max_length": max_len
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            print(Fore.RED + f"\nAPI Error: {response.status_code}")
            print(response.text)
            return

        result = response.json()

        if isinstance(result, list):
            print(Fore.GREEN + "\nSummary:\n")
            print(result[0]["summary_text"])
        elif "error" in result:
            print(Fore.RED + result["error"])
        else:
            print(result)

    except Exception as e:
        print(Fore.RED + f"Error: {e}")


def main():
    print(Fore.CYAN + "=" * 50)
    print("TEXT SUMMARIZATION TOOL")
    print("=" * 50)

    text = input("\nEnter text to summarize:\n\n")

    if not text.strip():
        print(Fore.RED + "Text cannot be empty.")
        return

    print("\nChoose Model")
    print("1. Pegasus (google/pegasus-xsum)")
    print("2. BART (facebook/bart-large-cnn)")

    choice = input("Enter choice (1/2) [Default=1]: ").strip()

    if choice not in MODELS:
        choice = "1"

    model = MODELS[choice]

    print("\nSummary Style")
    print("1. Standard (50-150 tokens)")
    print("2. Enhanced (80-200 tokens)")

    style = input("Choose style (1/2): ").strip()

    if style == "2":
        min_len = 80
        max_len = 200
    else:
        min_len = 50
        max_len = 150

    print(Fore.YELLOW + "\nGenerating summary...\n")

    summarize(text, model, min_len, max_len)


if __name__ == "__main__":
    main()