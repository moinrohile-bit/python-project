import requests

# -------------------------------
# PASTE YOUR HUGGING FACE TOKEN HERE
# -------------------------------
API_TOKEN = "YOUR_HUGGING_FACE_API_TOKEN"

API_URL = "https://api-inference.huggingface.co/models/mrm8488/bert-tiny-finetuned-sms-spam-detection"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}


def classify_message(message):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": message},
            timeout=30
        )

        if response.status_code != 200:
            print("\nAPI Error:")
            print(response.status_code)
            print(response.text)
            return

        result = response.json()

        # Some models take a few seconds to load
        if isinstance(result, dict) and "error" in result:
            print("\nAPI Message:")
            print(result["error"])
            print("Wait 20-30 seconds and try again.")
            return

        prediction = result[0]

        print("\n========== RESULT ==========")

        for item in prediction:
            label = item["label"]
            score = item["score"] * 100

            if label.upper() == "LABEL_1":
                print(f"Spam Confidence : {score:.2f}%")
            elif label.upper() == "LABEL_0":
                print(f"Safe Confidence : {score:.2f}%")
            else:
                print(f"{label}: {score:.2f}%")

        print("============================\n")

    except requests.exceptions.RequestException as e:
        print("Connection Error:", e)


def main():
    print("=" * 45)
    print(" AI Spam Message Classifier")
    print("=" * 45)

    while True:
        message = input("\nEnter a message:\n> ")

        if message.strip() == "":
            print("Please enter a message.")
            continue

        classify_message(message)

        again = input("Check another message? (yes/no): ").lower()

        if again not in ["yes", "y"]:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()