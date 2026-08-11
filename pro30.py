import pyttsx3
import random

# Create the speech engine
engine = pyttsx3.init()

# Starting settings
rate = 170
volume = 1.0

engine.setProperty("rate", rate)
engine.setProperty("volume", volume)


# Random phrases
def get_samples():
    samples = [
        "Hello! Nice to meet you!",
        "Have a great day!",
        "Python is awesome!",
        "Keep learning and keep coding!",
        "You are doing a great job!",
        "Never give up!",
        "Coding can be fun!",
        "Believe in yourself!",
        "Today is a great day to learn!",
        "Let's build something amazing!"
    ]

    return samples


# Random jokes
def get_joke():
    jokes = [
        "Why did the computer go to the doctor? Because it had a virus!",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why was the Python programmer confused? Because there were too many snakes!",
        "What do computers eat? Microchips!",
        "Why did the programmer quit his job? Because he didn't get arrays!"
    ]

    return random.choice(jokes)


# Speak function
def speak(text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()


# Main program
def main():

    global rate
    global volume

    speak("Hello! I am your AI assistant.")
    speak("You can ask me to tell a joke, change my speed or volume, or say exit to stop.")

    while True:

        command = input("\nYou: ").lower().strip()

        # Exit
        if command == "exit":
            speak("Goodbye! Have a great day!")
            break

        # Random phrase
        elif command in ["hello", "hi", "speak", "say something"]:
            speak(random.choice(get_samples()))

        # Tell a joke
        elif command == "tell a joke":
            speak(get_joke())

        # Speed up
        elif command == "speed up":
            rate += 30
            engine.setProperty("rate", rate)
            speak("I am speaking faster now.")

        # Slow down
        elif command == "slow down":
            rate -= 30

            # Prevent speech from becoming too slow
            if rate < 80:
                rate = 80

            engine.setProperty("rate", rate)
            speak("I am speaking slower now.")

        # Increase volume
        elif command == "increase volume":
            volume += 0.1

            # Maximum volume
            if volume > 1.0:
                volume = 1.0

            engine.setProperty("volume", volume)
            speak("Volume increased.")

        # Decrease volume
        elif command == "decrease volume":
            volume -= 0.1

            # Minimum volume
            if volume < 0.1:
                volume = 0.1

            engine.setProperty("volume", volume)
            speak("Volume decreased.")

        # Help command
        elif command == "help":
            speak("You can say hello, tell a joke, speed up, slow down, increase volume, decrease volume, or exit.")

        # Unknown command
        else:
            speak("I didn't quite catch that. Try again!")


# Run program
if __name__ == "__main__":
    main()