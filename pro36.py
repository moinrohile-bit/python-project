import os
import subprocess
from datetime import datetime

import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException


# ============================================================
# LANGUAGE LIST
# ============================================================

LANGUAGES = {
    "1": ("English", "en"),
    "2": ("Hindi", "hi"),
    "3": ("Tamil", "ta"),
    "4": ("Telugu", "te"),
    "5": ("Bengali", "bn"),
    "6": ("Marathi", "mr"),
    "7": ("Gujarati", "gu"),
    "8": ("Malayalam", "ml"),
    "9": ("Punjabi", "pa"),
    "10": ("French", "fr"),
    "11": ("German", "de"),
    "12": ("Spanish", "es"),
    "13": ("Japanese", "ja"),
    "14": ("Chinese", "zh-CN"),
    "15": ("Arabic", "ar"),
    "16": ("Russian", "ru"),
    "17": ("Portuguese", "pt"),
    "18": ("Korean", "ko"),
    "19": ("Italian", "it"),
}


# Google Speech Recognition language codes
SPEECH_CODES = {
    "en": "en-US",
    "hi": "hi-IN",
    "ta": "ta-IN",
    "te": "te-IN",
    "bn": "bn-IN",
    "mr": "mr-IN",
    "gu": "gu-IN",
    "ml": "ml-IN",
    "pa": "pa-IN",
    "fr": "fr-FR",
    "de": "de-DE",
    "es": "es-ES",
    "ja": "ja-JP",
    "zh-CN": "zh-CN",
    "ar": "ar-SA",
    "ru": "ru-RU",
    "pt": "pt-PT",
    "ko": "ko-KR",
}


# macOS voice names
# The exact voices available depend on the voices installed on your Mac.
MAC_VOICES = {
    "en": "Samantha",
    "hi": "Lekha",
    "ta": "Vani",
    "te": "Lekha",
    "bn": "Lekha",
    "mr": "Lekha",
    "gu": "Lekha",
    "ml": "Lekha",
    "pa": "Lekha",
    "fr": "Thomas",
    "de": "Anna",
    "es": "Monica",
    "ja": "Kyoko",
    "zh-CN": "Ting-Ting",
    "ar": "Maged",
    "ru": "Milena",
    "pt": "Joana",
    "ko": "Yuna",
}


# ============================================================
# TEXT TO SPEECH
# ============================================================

def speak(text, language="en"):
    """
    Uses the built-in macOS 'say' command.
    This avoids pyttsx3 compatibility problems on newer Python versions.
    """

    if not text:
        return

    print(f"\n🔊 Speaking: {text}")

    voice = MAC_VOICES.get(language, "Samantha")

    try:
        subprocess.run(
            ["say", "-v", voice, text],
            check=True
        )

    except subprocess.CalledProcessError:
        print(f"⚠️ Voice '{voice}' is not available on this Mac.")
        print("Using the default macOS voice instead.")

        subprocess.run(
            ["say", text],
            check=False
        )

    except Exception as error:
        print(f"❌ Text-to-speech error: {error}")


# ============================================================
# SHOW LANGUAGES
# ============================================================

def show_languages():
    print("\n" + "=" * 55)
    print("AVAILABLE LANGUAGES")
    print("=" * 55)

    for number, (name, code) in LANGUAGES.items():
        print(f"{number:>2}. {name:<15} ({code})")

    print("=" * 55)


# ============================================================
# SELECT LANGUAGE
# ============================================================

def select_language(message):
    while True:
        show_languages()

        choice = input(f"\n{message}: ").strip()

        if choice in LANGUAGES:
            name, code = LANGUAGES[choice]
            print(f"✅ Selected: {name}")
            return name, code

        print("❌ Invalid choice. Please select a number from the list.")


# ============================================================
# RECORD SPEECH
# ============================================================

def record_speech(language_code):
    """
    Records speech from the Mac microphone.
    """

    recognizer = sr.Recognizer()

    # Improve microphone sensitivity
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    speech_language = SPEECH_CODES.get(
        language_code,
        "en-US"
    )

    try:

        with sr.Microphone() as source:

            print("\n🎤 Microphone is ready.")
            print("Adjusting for background noise...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            print("🗣️ Speak now...")

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=15
            )

        print("🔄 Recognizing speech...")

        text = recognizer.recognize_google(
            audio,
            language=speech_language
        )

        print(f"\n📝 You said:")
        print(text)

        return text

    except sr.WaitTimeoutError:
        print("⏰ No speech detected.")
        return None

    except sr.UnknownValueError:
        print("❌ Sorry, I could not understand the speech.")
        return None

    except sr.RequestError as error:
        print(f"❌ Speech recognition service error: {error}")
        return None

    except Exception as error:
        print(f"❌ Microphone error: {error}")
        return None


# ============================================================
# AUTO DETECT LANGUAGE
# ============================================================

def detect_language(text):
    """
    Detects the language from recognized text.

    Note:
    Speech recognition itself needs a language to convert audio to text.
    This function detects the language AFTER the speech has been converted
    to text.
    """

    try:
        detected_code = detect(text)

        # Convert zh-cn/zh-tw etc. to our supported Chinese code
        if detected_code.startswith("zh"):
            detected_code = "zh-CN"

        for code, (name, _) in [
            (code, value)
            for value in LANGUAGES.values()
            for code in [value[1]]
        ]:
            if code == detected_code:
                return name, code

        return "Unknown", detected_code

    except LangDetectException:
        return "Unknown", None

    except Exception:
        return "Unknown", None


# ============================================================
# TRANSLATE
# ============================================================

def translate_text(text, target_language):
    """
    Translate text using Google Translate through deep-translator.
    """

    try:

        translator = GoogleTranslator(
            source="auto",
            target=target_language
        )

        translated = translator.translate(text)

        return translated

    except Exception as error:
        print(f"❌ Translation error: {error}")
        return None


# ============================================================
# SAVE TRANSLATION
# ============================================================

def save_translation(
    original_text,
    translated_text,
    source_language,
    target_language
):
    """
    Saves original speech and translation to a text file.
    """

    save_choice = input(
        "\n💾 Do you want to save this translation? (y/n): "
    ).strip().lower()

    if save_choice != "y":
        return

    filename = input(
        "Enter filename (press Enter for translation.txt): "
    ).strip()

    if not filename:
        filename = "translation.txt"

    if not filename.endswith(".txt"):
        filename += ".txt"

    try:

        with open(
            filename,
            "a",
            encoding="utf-8"
        ) as file:

            file.write("\n")
            file.write("=" * 60 + "\n")
            file.write(
                f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            file.write(
                f"Source Language: {source_language}\n"
            )
            file.write(
                f"Target Language: {target_language}\n"
            )
            file.write(
                f"Original Speech: {original_text}\n"
            )
            file.write(
                f"Translation: {translated_text}\n"
            )
            file.write("=" * 60 + "\n")

        print(f"✅ Translation saved to: {os.path.abspath(filename)}")

    except Exception as error:
        print(f"❌ Could not save file: {error}")


# ============================================================
# MAIN TRANSLATOR
# ============================================================

def translation_session():

    print("\n" + "=" * 60)
    print("       🎙️ SPEECH TRANSLATION SYSTEM")
    print("=" * 60)

    # --------------------------------------------------------
    # SOURCE LANGUAGE
    # --------------------------------------------------------

    print("\nSOURCE LANGUAGE")
    print("Choose the language you will speak.")

    source_name, source_code = select_language(
        "Select source language"
    )

    # --------------------------------------------------------
    # TARGET LANGUAGE
    # --------------------------------------------------------

    print("\nTARGET LANGUAGE")
    print("Choose the language you want to translate into.")

    target_name, target_code = select_language(
        "Select target language"
    )

    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("TRANSLATION READY")
    print("=" * 60)

    print(f"Source : {source_name}")
    print(f"Target : {target_name}")

    speak(
        f"Translation from {source_name} to {target_name} is ready.",
        "en"
    )

    # --------------------------------------------------------
    # RETRY LOOP
    # --------------------------------------------------------

    while True:

        original_text = record_speech(source_code)

        if original_text:
            break

        retry = input(
            "\nWould you like to try again? (y/n): "
        ).strip().lower()

        if retry != "y":
            print("\nExiting translation.")
            return

    # --------------------------------------------------------
    # DETECT LANGUAGE
    # --------------------------------------------------------

    detected_name, detected_code = detect_language(
        original_text
    )

    print("\n🌍 Detected language from text:")

    if detected_code:
        print(
            f"{detected_name} ({detected_code})"
        )
    else:
        print("Could not automatically determine language.")

    # --------------------------------------------------------
    # TRANSLATE
    # --------------------------------------------------------

    print("\n🔄 Translating...")

    translated_text = translate_text(
        original_text,
        target_code
    )

    if not translated_text:
        print("❌ Translation failed.")
        return

    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("TRANSLATION RESULT")
    print("=" * 60)

    print(f"Original ({source_name}):")
    print(original_text)

    print(f"\nTranslation ({target_name}):")
    print(translated_text)

    print("=" * 60)

    # --------------------------------------------------------
    # SPEAK TRANSLATION
    # --------------------------------------------------------

    speak(
        translated_text,
        target_code
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    save_translation(
        original_text,
        translated_text,
        source_name,
        target_name
    )


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        print("\n")
        print("=" * 60)
        print("       🎙️ SPEECH TRANSLATOR")
        print("=" * 60)

        print("1. Start Translation")
        print("2. Show Languages")
        print("3. Exit")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            try:
                translation_session()

            except KeyboardInterrupt:
                print("\n\n⚠️ Translation cancelled.")

            except Exception as error:
                print(
                    f"\n❌ Unexpected error: {error}"
                )

        elif choice == "2":

            show_languages()

        elif choice == "3":

            print("\n👋 Goodbye!")
            break

        else:

            print(
                "\n❌ Invalid choice. Please enter 1, 2, or 3."
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()