import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import speech_recognition as sr
import threading
import time
import itertools
import sys


# ==============================
# SETTINGS
# ==============================

SAMPLE_RATE = 16000       # 16 kHz
CHANNELS = 1              # Mono
BLOCK_SIZE = 1024

audio_data = []
recording = True


# ==============================
# SPINNER
# ==============================

def spinner():
    symbols = itertools.cycle(["|", "/", "-", "\\"])

    while recording:
        sys.stdout.write("\r🎤 Recording... " + next(symbols))
        sys.stdout.flush()
        time.sleep(0.1)

    sys.stdout.write("\r🛑 Recording stopped.     \n")


# ==============================
# AUDIO CALLBACK
# ==============================

def audio_callback(indata, frames, time_info, status):

    if status:
        print("\nAudio status:", status)

    audio_data.append(indata.copy())


# ==============================
# RECORD AUDIO
# ==============================

def record_audio():

    global recording

    print("\n===================================")
    print("        VOICE RECORDING")
    print("===================================")
    print("Speak into your microphone.")
    print("Press ENTER to stop recording.\n")

    recording = True

    # Start spinner
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    try:

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            blocksize=BLOCK_SIZE,
            callback=audio_callback
        ):

            # Wait for Enter
            input()

    except Exception as e:

        print("\n❌ Microphone error:")
        print(e)

    recording = False

    spinner_thread.join()


# ==============================
# SAVE WAV
# ==============================

def save_audio():

    if len(audio_data) == 0:

        print("❌ No audio recorded.")
        return None

    # Combine audio blocks
    recording = np.concatenate(audio_data, axis=0)

    # Convert stereo/2D array to mono
    recording = recording[:, 0]

    # Save WAV
    write(
        "my_audio.wav",
        SAMPLE_RATE,
        recording
    )

    print("💾 Saved audio as: my_audio.wav")

    return recording


# ==============================
# TRANSCRIBE AUDIO
# ==============================

def transcribe_audio():

    recognizer = sr.Recognizer()

    print("\n📝 Transcribing your speech...")

    try:

        with sr.AudioFile("my_audio.wav") as source:

            audio = recognizer.record(source)

        # Google Speech Recognition
        text = recognizer.recognize_google(audio)

        print("\n===================================")
        print("          TRANSCRIPTION")
        print("===================================")
        print(text)
        print("===================================\n")

        # Save transcription
        with open(
            "my_transcript.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(text)

        print("💾 Saved transcription as: my_transcript.txt")

        return text

    except sr.UnknownValueError:

        text = "Google Speech Recognition could not understand the audio."

        print("\n❌", text)

        with open(
            "my_transcript.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(text)

        return text

    except sr.RequestError as error:

        text = "Could not connect to Google's Speech Recognition service."

        print("\n❌", text)
        print("Error:", error)

        with open(
            "my_transcript.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(text)

        return text

    except Exception as error:

        print("\n❌ Transcription error:")
        print(error)

        return None


# ==============================
# DISPLAY WAVEFORM
# ==============================

def show_waveform(recording):

    print("\n📈 Creating waveform...")

    # Time values for x-axis
    duration = len(recording) / SAMPLE_RATE

    time_axis = np.linspace(
        0,
        duration,
        len(recording)
    )

    plt.figure(figsize=(12, 5))

    plt.plot(
        time_axis,
        recording
    )

    plt.title("Waveform of My Voice")

    plt.xlabel("Time (seconds)")

    plt.ylabel("Amplitude")

    plt.grid(True)

    plt.tight_layout()

    plt.show()


# ==============================
# MAIN PROGRAM
# ==============================

def main():

    print("\n")
    print("======================================")
    print("       PYTHON VOICE PROJECT")
    print("======================================")
    print("Microphone: Ready")
    print("Sample Rate: 16000 Hz")
    print("Channels: Mono")
    print("======================================")

    # Start recording
    record_audio()

    # Save recording
    recording = save_audio()

    if recording is None:
        return

    # Transcribe
    transcribe_audio()

    # Display waveform
    show_waveform(recording)

    print("\n✅ Project completed successfully!")
    print("Files created:")
    print("  📁 my_audio.wav")
    print("  📁 my_transcript.txt")


# ==============================
# START PROGRAM
# ==============================

if __name__ == "__main__":
    main()