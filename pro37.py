import speech_recognition as sr
import subprocess
import random
from datetime import datetime
import os
import re


# ============================================================
# SETTINGS
# ============================================================

NAME_FILE = "assistant_name.txt"

# Mac voices
MALE_VOICE = "Alex"
FEMALE_VOICE = "Samantha"

# Current voice
current_voice = FEMALE_VOICE


# ============================================================
# 5 RANDOM FACTS
# ============================================================

FACTS = [
    "Honey never spoils. Archaeologists have found edible honey in ancient Egyptian tombs.",
    
    "Octopuses have three hearts.",
    
    "Bananas are technically berries, but strawberries are not botanical berries.",
    
    "A day on Venus is longer than a year on Venus.",
    
    "The Eiffel Tower can become slightly taller during hot weather because metal expands."
]


# ============================================================
# LOAD SAVED NAME
# ============================================================

def load_name():
    """
    Loads the user's saved name from a text file.
    """

    try:
        if os.path.exists(NAME_FILE):

            with open(
                NAME_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                name = file.read().strip()

                if name:
                    return name

    except Exception as error:
        print(f"Could not load saved name: {error}")

    return None


# ============================================================
# SAVE NAME
# ============================================================

def save_name(name):
    """
    Saves the user's name so it can be remembered later.
    """

    try:

        with open(
            NAME_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(name)

        return True

    except Exception as error:

        print(f"Could not save name: {error}")
        return False


# ============================================================
# TEXT TO SPEECH
# ============================================================

def speak(text):
    """
    Uses macOS built-in 'say' command.
    """

    global current_voice

    print(f"Assistant: {text}")

    try:

        subprocess.run(
            [
                "say",
                "-v",
                current_voice,
                text
            ],
            check=True
        )

    except Exception as error:

        print(f"TTS error: {error}")

        # Fallback to Mac default voice
        try:

            subprocess.run(
                ["say", text],
                check=False
            )

        except Exception as fallback_error:

            print(
                f"Could not use Mac text-to-speech: "
                f"{fallback_error}"
            )


# ============================================================
# SPEECH RECOGNITION
# ============================================================

def listen():
    """
    Listen to the microphone and convert speech to text.
    """

    recognizer = sr.Recognizer()

    # Helps with background noise
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True

    # How long to wait after speech before stopping
    recognizer.pause_threshold = 0.8

    try:

        with sr.Microphone() as source:

            print("\n🎤 Listening...")
            print("Speak now...")

            # Adjust microphone to background noise
            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            try:

                audio = recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=15
                )

            except sr.WaitTimeoutError:

                print("⏰ No speech detected.")
                speak(
                    "I did not hear anything. "
                    "Please try again."
                )

                return None

        print("🔄 Recognizing...")

        try:

            text = recognizer.recognize_google(
                audio,
                language="en-US"
            )

            text = text.strip()

            if not text:

                print("No words detected.")

                speak(
                    "I could not detect any words. "
                    "Please try again."
                )

                return None

            print(f"You: {text}")

            return text.lower()

        except sr.UnknownValueError:

            print("❌ Speech was unclear.")

            speak(
                "Sorry, I could not understand you. "
                "Please try again."
            )

            return None

        except sr.RequestError as error:

            print(
                f"❌ Speech recognition service error: "
                f"{error}"
            )

            speak(
                "There was a problem with the speech "
                "recognition service."
            )

            return None

    except OSError as error:

        print(f"❌ Microphone error: {error}")

        speak(
            "I cannot access the microphone. "
            "Please check your microphone permissions."
        )

        return None

    except Exception as error:

        print(f"❌ Unexpected microphone error: {error}")

        speak(
            "Something went wrong while listening."
        )

        return None


# ============================================================
# DATE COMMAND
# ============================================================

def tell_date():

    today = datetime.now()

    formatted_date = today.strftime(
        "%B %d, %Y"
    )

    speak(
        f"Today is {formatted_date}."
    )


# ============================================================
# SAVE USER NAME
# ============================================================

def process_name_command(command):
    """
    Handles:
        my name is Moin
        my name is John
    """

    pattern = r"my name is (.+)"

    match = re.search(
        pattern,
        command,
        re.IGNORECASE
    )

    if not match:
        return False

    name = match.group(1).strip()

    # Remove unnecessary punctuation
    name = name.strip(" .,!?")

    if not name:

        speak(
            "I did not catch your name. "
            "Please say, my name is followed by your name."
        )

        return True

    # Capitalize each word
    name = name.title()

    if save_name(name):

        speak(
            f"Nice to meet you, {name}. "
            f"I will remember your name."
        )

    else:

        speak(
            f"Nice to meet you, {name}. "
            f"I could not save your name permanently."
        )

    return True


# ============================================================
# HELLO COMMAND
# ============================================================

def say_hello():

    name = load_name()

    if name:

        speak(
            f"Hi {name}! How can I help you?"
        )

    else:

        speak(
            "Hi! How can I help you?"
        )


# ============================================================
# RANDOM FACT COMMAND
# ============================================================

def tell_fact():

    fact = random.choice(FACTS)

    speak(
        f"Here is a fun fact. {fact}"
    )


# ============================================================
# CHANGE TO MALE VOICE
# ============================================================

def use_male_voice():

    global current_voice

    current_voice = MALE_VOICE

    speak(
        "Male voice selected."
    )


# ============================================================
# CHANGE TO FEMALE VOICE
# ============================================================

def use_female_voice():

    global current_voice

    current_voice = FEMALE_VOICE

    speak(
        "Female voice selected."
    )


# ============================================================
# PROCESS COMMAND
# ============================================================

def process_command(command):
    """
    Processes the user's command.
    Returns False when the assistant should exit.
    """

    if not command:
        return True

    command = command.lower().strip()

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    if (
        command == "exit"
        or command == "quit"
        or command == "goodbye"
        or command == "stop"
    ):

        speak("Goodbye! Have a great day.")
        return False

    # --------------------------------------------------------
    # NAME
    # --------------------------------------------------------

    if command.startswith("my name is"):

        process_name_command(command)
        return True

    # --------------------------------------------------------
    # HELLO
    # --------------------------------------------------------

    if (
        command == "hello"
        or command == "hi"
        or command == "hey"
        or "hello" in command
    ):

        say_hello()
        return True

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    if (
        command == "date"
        or "today's date" in command
        or "todays date" in command
        or "what is the date" in command
        or "what's the date" in command
        or "what date is it" in command
    ):

        tell_date()
        return True

    # --------------------------------------------------------
    # FACT
    # --------------------------------------------------------

    if (
        command == "fact"
        or "fun fact" in command
        or "tell me a fact" in command
    ):

        tell_fact()
        return True

    # --------------------------------------------------------
    # MALE VOICE
    # --------------------------------------------------------

    if (
        "use male voice" in command
        or command == "male voice"
        or command == "male"
    ):

        use_male_voice()
        return True

    # --------------------------------------------------------
    # FEMALE VOICE
    # --------------------------------------------------------

    if (
        "use female voice" in command
        or command == "female voice"
        or command == "female"
    ):

        use_female_voice()
        return True

    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    if (
        command == "help"
        or "what can you do" in command
    ):

        speak(
            "You can ask me for the date, "
            "tell me your name, ask for a fun fact, "
            "change my voice, or say goodbye."
        )

        return True

    # --------------------------------------------------------
    # UNKNOWN COMMAND
    # --------------------------------------------------------

    speak(
        "Sorry, I do not understand that command. "
        "Please try again."
    )

    return True


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("           PYTHON VOICE ASSISTANT")
    print("=" * 60)

    print("\nAvailable commands:")
    print("• hello")
    print("• date")
    print("• my name is <name>")
    print("• fact")
    print("• use male voice")
    print("• use female voice")
    print("• help")
    print("• goodbye / exit / quit")
    print("=" * 60)

    # Load previously saved name
    saved_name = load_name()

    if saved_name:

        print(
            f"\n👤 Saved user name: {saved_name}"
        )

    else:

        print("\n👤 No name saved yet.")

    # Startup message
    speak(
        "Voice assistant activated. "
        "Say a command."
    )

    # --------------------------------------------------------
    # MAIN LOOP
    # --------------------------------------------------------

    while True:

        try:

            command = listen()

            # If no speech was detected,
            # automatically return to listening.
            if command is None:

                print(
                    "\n🔁 Waiting for another command..."
                )

                continue

            should_continue = process_command(
                command
            )

            if not should_continue:
                break

        except KeyboardInterrupt:

            print(
                "\n\nAssistant stopped by user."
            )

            speak("Goodbye.")
            break

        except Exception as error:

            print(
                f"\n❌ Unexpected error: {error}"
            )

            speak(
                "An unexpected error occurred. "
                "I am ready to try again."
            )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()