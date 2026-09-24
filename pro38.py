import speech_recognition as sr
from deep_translator import GoogleTranslator
import subprocess
import sys


# ============================================================
# TARGET LANGUAGES
# ============================================================

LANGUAGES = {
    "1": ("Hindi", "hi", "Lekha"),
    "2": ("Tamil", "ta", "Vani"),
    "3": ("Telugu", "te", "Lekha"),
    "4": ("Bengali", "bn", "Lekha"),
    "5": ("Marathi", "mr", "Lekha"),
    "6": ("Gujarati", "gu", "Lekha"),
    "7": ("Malayalam", "ml", "Lekha"),
    "8": ("Punjabi", "pa", "Lekha"),
    "9": ("French", "fr", "Thomas"),
    "10": ("German", "de", "Anna"),
    "11": ("Spanish", "es", "Monica"),
    "12": ("Japanese", "ja", "Kyoko"),
    "13": ("Chinese", "zh-CN", "Ting-Ting"),
    "14": ("Arabic", "ar", "Maged"),
    "15": ("Russian", "ru", "Milena"),
    "16": ("Portuguese", "pt", "Joana"),
    "17": ("Italian", "it", "Alice"),
    "18": ("Korean", "ko", "Yuna"),
}


# ============================================================
# SHOW LANGUAGES
# ============================================================

def show_languages():
    print("\n" + "=" * 55)
    print("             TARGET LANGUAGES")
    print("=" * 55)

    for number, (name, code, voice) in LANGUAGES.items():
        print(f"{number:>2}. {name:<15} ({code})")

    print("=" * 55)


# ============================================================
# SELECT LANGUAGE
# ============================================================

def select_language():

    while True:

        show_languages()

        choice = input(
            "\nSelect target language: "
        ).strip()

        if choice in LANGUAGES:

            name, code, voice = LANGUAGES[choice]

            print(f"\nSelected: {name}")

            return name, code, voice

        print(
            "\n❌ Invalid selection."
            "\nPlease enter a number from the menu."
        )


# ============================================================
# MAC TEXT TO SPEECH
# ============================================================

def speak(text, voice):

    print("\n🔊 Speaking translation...")
    print(f"Translation: {text}")

    try:

        # Try the selected Mac voice
        result = subprocess.run(
            [
                "say",
                "-v",
                voice,
                text
            ],
            capture_output=True,
            text=True
        )

        # If voice doesn't exist, use default Mac voice
        if result.returncode != 0:

            print(
                f"⚠️ Voice '{voice}' is not available."
            )

            print(
                "Using the default Mac voice instead."
            )

            subprocess.run(
                ["say", text],
                check=False
            )

    except Exception as error:

        print(
            f"❌ Text-to-speech error: {error}"
        )


# ============================================================
# RECORD ENGLISH SPEECH
# ============================================================

def listen_to_english():

    recognizer = sr.Recognizer()

    # Improve microphone sensitivity
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    try:

        with sr.Microphone() as source:

            print("\n🎤 Microphone ready.")
            print("Adjusting for background noise...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            print("\n🗣️ Speak in English now...")

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=15
            )

        print("\n🔄 Converting speech to text...")

        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print("\n" + "=" * 55)
        print("RECOGNIZED ENGLISH")
        print("=" * 55)
        print(text)
        print("=" * 55)

        return text

    except sr.WaitTimeoutError:

        print(
            "\n⏰ No speech detected."
        )

        return None

    except sr.UnknownValueError:

        print(
            "\n❌ I could not understand the speech."
        )

        return None

    except sr.RequestError as error:

        print(
            "\n❌ Speech recognition service error."
        )

        print(f"Details: {error}")

        return None

    except OSError as error:

        print(
            "\n❌ Microphone error."
        )

        print(f"Details: {error}")

        print(
            "\nCheck that VS Code has permission "
            "to access your microphone."
        )

        return None

    except Exception as error:

        print(
            "\n❌ Unexpected error while recording."
        )

        print(f"Details: {error}")

        return None


# ============================================================
# TRANSLATE TEXT
# ============================================================

def translate_text(text, target_language):

    try:

        print("\n🔄 Translating...")

        translator = GoogleTranslator(
            source="en",
            target=target_language
        )

        translation = translator.translate(text)

        if not translation:

            print(
                "\n❌ Translation returned empty text."
            )

            return None

        print("\n" + "=" * 55)
        print("TRANSLATION")
        print("=" * 55)
        print(translation)
        print("=" * 55)

        return translation

    except Exception as error:

        print(
            "\n❌ Translation error."
        )

        print(f"Details: {error}")

        return None


# ============================================================
# ONE COMPLETE TRANSLATION
# ============================================================

def translation_session():

    print("\n" + "=" * 60)
    print("          🎙️ VOICE-TO-VOICE TRANSLATOR")
    print("=" * 60)

    print(
        "\nSpeak English and the assistant will translate "
        "your speech into the selected language."
    )

    # --------------------------------------------------------
    # SELECT TARGET
    # --------------------------------------------------------

    target_name, target_code, target_voice = (
        select_language()
    )

    # --------------------------------------------------------
    # RECORD SPEECH
    # --------------------------------------------------------

    original_text = listen_to_english()

    if original_text is None:
        return

    # --------------------------------------------------------
    # TRANSLATE
    # --------------------------------------------------------

    translated_text = translate_text(
        original_text,
        target_code
    )

    if translated_text is None:
        return

    # --------------------------------------------------------
    # SPEAK TRANSLATION
    # --------------------------------------------------------

    print(
        f"\n🌍 Target language: {target_name}"
    )

    speak(
        translated_text,
        target_voice
    )


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        print("\n")
        print("=" * 60)
        print("             VOICE TRANSLATOR")
        print("=" * 60)

        print("1. Start voice translation")
        print("2. Show target languages")
        print("3. Exit")

        print("=" * 60)

        choice = input(
            "\nEnter your choice: "
        ).strip()

        # ----------------------------------------------------
        # START
        # ----------------------------------------------------

        if choice == "1":

            while True:

                translation_session()

                retry = input(
                    "\nTry another translation? (y/n): "
                ).strip().lower()

                if retry != "y":
                    break

        # ----------------------------------------------------
        # SHOW LANGUAGES
        # ----------------------------------------------------

        elif choice == "2":

            show_languages()

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        elif choice == "3":

            print(
                "\n👋 Thank you for using "
                "the Voice Translator!"
            )

            sys.exit(0)

        # ----------------------------------------------------
        # INVALID
        # ----------------------------------------------------

        else:

            print(
                "\n❌ Invalid choice."
            )

            print(
                "Please enter 1, 2, or 3."
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()