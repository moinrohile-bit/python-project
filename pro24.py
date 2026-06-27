import requests

# -----------------------------
# Paste your Hugging Face API Token here
# Example: hf_xxxxxxxxxxxxxxxxxxxxxxxxx
# -----------------------------
API_TOKEN = "YOUR_HUGGING_FACE_API_TOKEN"

API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}


def analyze_sentiment(text):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": text},
            timeout=30
        )

        if response.status_code != 200:
            print("\nError:", response.status_code)
            print(response.text)
            return

        result = response.json()

        # Model may still be loading
        if isinstance(result, dict) and "error" in result:
            print("\nAPI Message:")
            print(result["error"])
            print("Wait about 20 seconds and try again.")
            return

        predictions = result[0]

        print("\n========== SENTIMENT RESULT ==========")

        highest = max(predictions, key=lambda x: x["score"])

        for item in predictions:
            label = item["label"]
            score = item["score"] * 100
            print(f"{label:<10}: {score:.2f}%")

        print("--------------------------------------")
        print(f"Overall Sentiment: {highest['label']}")
        print("======================================\n")

    except requests.exceptions.RequestException as e:
        print("Connection Error:", e)


def main():
    print("=" * 45)
    print(" Hugging Face Sentiment Analyzer")
    print("=" * 45)

    while True:
        text = input("\nEnter text to analyze:\n> ")

        if text.strip() == "":
            print("Please enter some text.")
            continue

        analyze_sentiment(text)

        again = input("Analyze another sentence? (yes/no): ").strip().lower()

        if again not in ["yes", "y"]:
            print("\nThank you for using the Sentiment Analyzer!")
            break


if __name__ == "__main__":
    main()