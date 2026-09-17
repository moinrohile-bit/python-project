import speech_recognition as sr
import pyttsx3
from datetime import datetime


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()


def get_audio():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Speak now...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)

            print(f"You said: {command}")

            return command.lower()

        except sr.UnknownValueError:
            print("Could not understand what you said.")

        except sr.RequestError as e:
            print(f"Speech recognition API error: {e}")

    except Exception as e:
        print(f"Microphone error: {e}")

    return ""


def respond_to_command(command):

    if "hello" in command:
        speak("Hi there! How can I help you today?")

    elif "your name" in command:
        speak("I am your Python voice assistant.")

    elif "time" in command:
        now = datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")

    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        return False

    else:
        speak("I'm not sure how to help with that.")

    return True


def main():

    speak("Voice assistant activated. Say something!")

    while True:

        command = get_audio()

        if command:
            if not respond_to_command(command):
                break


if __name__ == "__main__":
    main()