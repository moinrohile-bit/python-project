from textblob import TextBlob
import datetime

# Store conversation history
conversation_history = []

# Sentiment counters
positive_count = 0
negative_count = 0
neutral_count = 0


def analyze_sentiment(text):
    """Analyze user sentiment using TextBlob"""

    global positive_count, negative_count, neutral_count

    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        positive_count += 1
        return "positive"
    elif polarity < 0:
        negative_count += 1
        return "negative"
    else:
        neutral_count += 1
        return "neutral"


def chatbot_response(sentiment):
    """Return chatbot response based on sentiment"""

    if sentiment == "positive":
        return "😊 You sound happy today!"
    
    elif sentiment == "negative":
        return "💙 I'm sorry you're feeling that way."
    
    else:
        return "😐 I see. Tell me more."


def save_conversation(user_text, bot_text):
    """Save chat history"""

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conversation_history.append({
        "time": timestamp,
        "user": user_text,
        "bot": bot_text
    })


def show_history():
    """Display conversation history"""

    print("\n📜 Conversation History:")
    print("-" * 40)

    for chat in conversation_history:
        print(f"[{chat['time']}]")
        print(f"You: {chat['user']}")
        print(f"Bot: {chat['bot']}")
        print("-" * 40)


def show_sentiment_stats():
    """Display sentiment statistics"""

    print("\n📊 Sentiment Statistics")
    print("-" * 30)
    print(f"Positive Messages : {positive_count}")
    print(f"Negative Messages : {negative_count}")
    print(f"Neutral Messages  : {neutral_count}")


def chatbot():
    """Main chatbot loop"""

    print("🤖 Welcome to the AI Sentiment Chatbot!")
    print("Type 'history' to see chat history.")
    print("Type 'stats' to see sentiment statistics.")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You: ")

        # Exit command
        if user_input.lower() == "exit":
            print("\n👋 Goodbye!")
            break

        # Show history
        elif user_input.lower() == "history":
            show_history()
            continue

        # Show stats
        elif user_input.lower() == "stats":
            show_sentiment_stats()
            continue

        # Analyze sentiment
        sentiment = analyze_sentiment(user_input)

        # Generate response
        bot_reply = chatbot_response(sentiment)

        # Display response
        print("Bot:", bot_reply)

        # Save conversation
        save_conversation(user_input, bot_reply)


# Run chatbot
chatbot()