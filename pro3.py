import os
import re
import sys


def clean_input(user_text):
    """Cleans user input to improve matching (basic NLP preprocessing)."""
    # Convert to lowercase
    text = user_text.lower().strip()
    # Remove punctuation using regex
    text = re.sub(r"[^\w\s]", "", text)
    return text


def get_bot_response(cleaned_text):
    """Rule-based engine matching keywords to predefined responses."""
    # Dictionary mapping intent keywords to responses
    rules = {
        ("hello", "hi", "hey"): "Greetings! How can I assist you today?",
        ("help", "support", "commands"): (
            "I can help you with system info or just chat. "
            "Try asking 'what is your name' or 'system info'."
        ),
        ("name", "identity"): "I am MacBot, a Python-powered assistant.",
        (
            "mac",
            "macos",
            "system info",
        ): "You are running this on macOS. Python is working perfectly!",
        ("bye", "exit", "quit"): "Goodbye! Have a great day.",
    }

    # Search for keywords in the cleaned text
    for keywords, response in rules.items():
        if any(keyword in cleaned_text for keyword in keywords):
            return response

    # Default fallback response if no rules match
    return "I am not sure I understand. Could you rephrase that? (Type 'help' for options)"


def main():
    """Main application loop."""
    # Clear the terminal screen using macOS system command
    os.system("clear")

    print("=========================================")
    print("🤖 Welcome to MacBot (Rule-Based Chatbot) ")
    print("Type 'exit' or 'quit' to end the chat.    ")
    print("=========================================\n")

    while True:
        try:
            # Capture user input
            user_raw = input("You: ")

            # Fast exit check before preprocessing
            if user_raw.strip().lower() in ["exit", "quit"]:
                print("Bot: Goodbye!")
                break

            # 1. Improve Input Handling (NLP concept: Text Normalization)
            cleaned = clean_input(user_raw)

            # Ignore empty inputs
            if not cleaned:
                continue

            # 2. Process Intent and Get Response
            response = get_bot_response(cleaned)
            print(f"Bot: {response}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nBot: Session interrupted. Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    main()
