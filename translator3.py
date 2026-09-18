import speech_recognition as sr
import pyttsx3
import requests


# -----------------------------
# Text to Speech
# -----------------------------
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)

        print("Speaking:", text)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print("Text-to-speech error:", e)


# -----------------------------
# Speech to Text
# -----------------------------
def speech_to_text():

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            print("\nPlease speak in English...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(source)

        print("Recognising speech...")

        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print("You said:", text)

        return text

    except sr.UnknownValueError:
        print("Could not understand the audio.")

    except sr.RequestError as e:
        print("Speech recognition error:", e)

    except Exception as e:
        print("Microphone error:", e)

    return ""


# -----------------------------
# Translation
# -----------------------------
def translate_text(text, target_language):

    try:

        url = "https://translate.googleapis.com/translate_a/single"

        params = {
            "client": "gtx",
            "sl": "en",
            "tl": target_language,
            "dt": "t",
            "q": text
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        translated_text = ""

        for item in data[0]:
            if item[0]:
                translated_text += item[0]

        print("Translated text:", translated_text)

        return translated_text

    except requests.exceptions.RequestException as e:
        print("Translation connection error:", e)

    except Exception as e:
        print("Translation error:", repr(e))

    return ""


# -----------------------------
# Language Selection
# -----------------------------
def display_language_options():

    print("\nAvailable Translation Languages")
    print("--------------------------------")
    print("1. Hindi")
    print("2. Tamil")
    print("3. Telugu")
    print("4. Bengali")
    print("5. Marathi")
    print("6. Gujarati")
    print("7. Malayalam")
    print("8. Punjabi")

    choice = input("\nSelect target language (1-8): ")

    language_dict = {
        "1": "hi",
        "2": "ta",
        "3": "te",
        "4": "bn",
        "5": "mr",
        "6": "gu",
        "7": "ml",
        "8": "pa"
    }

    return language_dict.get(choice)


# -----------------------------
# Main
# -----------------------------
def main():

    target_language = display_language_options()

    if not target_language:
        print("Invalid language selection.")
        return

    original_text = speech_to_text()

    if not original_text:
        return

    translated_text = translate_text(
        original_text,
        target_language
    )

    if not translated_text:
        print("Translation failed.")
        return

    print("\n================================")
    print("Original   :", original_text)
    print("Translated :", translated_text)
    print("================================")

    speak(translated_text)


if __name__ == "__main__":
    main()