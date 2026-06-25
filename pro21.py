import requests
import random
import html

API_URL = "https://opentdb.com/api.php?amount=5&type=multiple"

def fetch_questions():
    try:
        response = requests.get(API_URL, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data["response_code"] == 0:
                return data["results"]
            else:
                print("Error: No questions returned from API.")
                return []

        else:
            print(f"Error: Status Code {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print("Request Failed:", e)
        return []


def run_quiz():
    questions = fetch_questions()

    if not questions:
        return

    score = 0

    print("\n===== TRIVIA QUIZ GAME =====\n")

    for i, q in enumerate(questions, start=1):

        question = html.unescape(q["question"])
        correct_answer = html.unescape(q["correct_answer"])

        options = [html.unescape(ans) for ans in q["incorrect_answers"]]
        options.append(correct_answer)

        random.shuffle(options)

        correct_index = options.index(correct_answer) + 1

        print(f"\nQuestion {i}:")
        print(question)
        print()

        for idx, option in enumerate(options, start=1):
            print(f"{idx}. {option}")

        while True:
            answer = input("\nEnter your answer (1-4): ")

            if answer in ["1", "2", "3", "4"]:
                answer = int(answer)
                break
            else:
                print("Invalid input! Please enter 1, 2, 3, or 4.")

        if answer == correct_index:
            print("✅ Correct!")
            score += 1
        else:
            print("❌ Wrong!")
            print(f"Correct Answer: {correct_answer}")

        print("-" * 50)

    print("\n===== QUIZ COMPLETED =====")
    print(f"Your Final Score: {score} / {len(questions)}")

    percentage = (score / len(questions)) * 100

    print(f"Percentage: {percentage:.0f}%")

    if percentage >= 80:
        print("🏆 Excellent!")
    elif percentage >= 50:
        print("👍 Good Job!")
    else:
        print("📚 Keep Practicing!")


if __name__ == "__main__":
    run_quiz()