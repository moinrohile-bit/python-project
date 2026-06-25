import requests
import html

def get_joke():
    url = "https://official-joke-api.appspot.com/random_joke"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            print("\n😂 RANDOM JOKE")
            print("-" * 50)
            print("Setup:")
            print(data["setup"])
            print("\nPunchline:")
            print(data["punchline"])

        else:
            print(f"Error: API returned status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


def get_cat_fact():
    url = "https://catfact.ninja/fact"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            print("\n🐱 CAT FACT")
            print("-" * 50)
            print(data["fact"])

        else:
            print(f"Error: API returned status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


def get_trivia():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            question_data = data["results"][0]

            question = html.unescape(question_data["question"])
            correct_answer = html.unescape(question_data["correct_answer"])

            print("\n🧠 TRIVIA QUESTION")
            print("-" * 50)
            print("Question:")
            print(question)
            print("\nAnswer:")
            print(correct_answer)

        else:
            print(f"Error: API returned status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


def main():
    print("=" * 50)
    print("PUBLIC API DATA FETCHER")
    print("=" * 50)
    print("1. Random Joke")
    print("2. Cat Fact")
    print("3. Trivia Question")

    choice = input("\nEnter your choice (1-3): ")

    if choice == "1":
        get_joke()

    elif choice == "2":
        get_cat_fact()

    elif choice == "3":
        get_trivia()

    else:
        print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()