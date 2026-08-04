import os
import speech_recognition as sr
from deep_translator import GoogleTranslator


# -----------------------------
# Language Dictionary
# -----------------------------
LANGUAGES = {
    "1": ("Hindi", "hi"),
    "2": ("Tamil", "ta"),
    "3": ("Telugu", "te"),
    "4": ("Bengali", "bn"),
    "5": ("Marathi", "mr"),
    "6": ("Gujarati", "gu"),
    "7": ("Malayalam", "ml"),
    "8": ("Punjabi", "pa"),
    "9": ("French", "fr"),
    "10": ("German", "de"),
    "11": ("Spanish", "es"),
    "12": ("Japanese", "ja"),
    "13": ("Chinese", "zh-CN")
}


# -----------------------------
# Display Language Menu
# -----------------------------
def choose_language():
    print("\nAvailable Languages\n")

    for key, value in LANGUAGES.items():
        print(f"{key}. {value[0]}")

    choice = input("\nSelect language: ").strip()

    if choice in LANGUAGES:
        return LANGUAGES[choice]

    print("Invalid choice. Defaulting to Hindi.")
    return LANGUAGES["1"]


# -----------------------------
# Speech Recognition
# -----------------------------
def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nSpeak in English...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(source)

    try:
        print("Recognizing...")

        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print(f"\nYou said: {text}")

        return text

    except sr.UnknownValueError:
        print("Could not understand speech.")

    except sr.RequestError as e:
        print("Speech Recognition Error:", e)

    return ""


# -----------------------------
# Translation
# -----------------------------
def translate_text(text, target):
    translated = GoogleTranslator(
        source="en",
        target=target
    ).translate(text)

    return translated


# -----------------------------
# Speak Using macOS
# -----------------------------
def speak(text):
    text = text.replace('"', '\\"')
    os.system(f'say "{text}"')


# -----------------------------
# Main Program
# -----------------------------
def main():

    print("=" * 50)
    print("Speech Translator")
    print("=" * 50)

    language_name, language_code = choose_language()

    original_text = speech_to_text()

    if not original_text:
        return

    print("\nTranslating...")

    translated = translate_text(
        original_text,
        language_code
    )

    print(f"\nTranslated ({language_name}):")
    print(translated)

    print("\nSpeaking Translation...")

    speak(translated)

    print("\nDone!")


if __name__ == "__main__":
    main()