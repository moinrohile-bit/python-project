import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import speech_recognition as sr
import threading

# -----------------------------
# Settings
# -----------------------------
RATE = 16000              # 16 kHz
CHANNELS = 1             # Mono
FRAMES_PER_BUFFER = 1024

recording = []
recording_finished = False


# -----------------------------
# Audio callback
# -----------------------------
def audio_callback(indata, frames, time, status):
    if status:
        print("Audio status:", status)

    recording.append(indata.copy())


# -----------------------------
# Recording function
# -----------------------------
def record_audio():
    global recording_finished

    print("\n🎤 Recording started...")
    print("Speak now.")
    print("Press ENTER to stop recording.\n")

    with sd.InputStream(
        samplerate=RATE,
        channels=CHANNELS,
        dtype="int16",
        blocksize=FRAMES_PER_BUFFER,
        callback=audio_callback
    ):
        input()

    recording_finished = True
    print("\n🛑 Recording stopped.")


# -----------------------------
# Save WAV file
# -----------------------------
def save_audio():
    if not recording:
        print("No audio was recorded.")
        return None

    audio_data = np.concatenate(recording, axis=0)

    # Make sure audio is mono
    audio_data = audio_data[:, 0]

    wav.write("speech.wav", RATE, audio_data)

    print("💾 Audio saved as: speech.wav")

    return audio_data


# -----------------------------
# Show waveform
# -----------------------------
def show_waveform(audio_data):

    # Convert samples to seconds
    time_axis = np.arange(len(audio_data)) / RATE

    plt.figure(figsize=(12, 5))

    plt.plot(time_axis, audio_data)

    plt.title("Waveform of Your Voice")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")

    plt.grid(True)
    plt.tight_layout()

    print("📈 Showing waveform...")

    plt.show()


# -----------------------------
# Speech transcription
# -----------------------------
def transcribe_audio():

    recognizer = sr.Recognizer()

    try:
        print("\n📝 Transcribing audio...")

        with sr.AudioFile("speech.wav") as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        print("\n========== TRANSCRIPTION ==========")
        print(text)
        print("===================================\n")

        # Save transcription
        with open("speech.txt", "w", encoding="utf-8") as file:
            file.write(text)

        print("💾 Transcription saved as: speech.txt")

        return text

    except sr.UnknownValueError:
        text = "Sorry, I could not understand the audio."

        print("\n❌", text)

        with open("speech.txt", "w", encoding="utf-8") as file:
            file.write(text)

        return text

    except sr.RequestError as error:
        text = "Speech recognition service is unavailable."

        print("\n❌", text)
        print("Error:", error)

        with open("speech.txt", "w", encoding="utf-8") as file:
            file.write(text)

        return text

    except Exception as error:
        print("\n❌ An unexpected error occurred:")
        print(error)

        return None


# -----------------------------
# Main program
# -----------------------------
def main():

    print("====================================")
    print("       SAY AND SEE - MAC")
    print("====================================")

    try:
        # Start recording immediately
        record_audio()

        # Save audio
        audio_data = save_audio()

        if audio_data is None:
            return

        # Transcribe
        transcribe_audio()

        # Show waveform
        show_waveform(audio_data)

        print("\n✅ Program finished.")

    except KeyboardInterrupt:
        print("\n\nProgram stopped.")

    except Exception as error:
        print("\n❌ Error:")
        print(error)


# -----------------------------
# Run program
# -----------------------------
if __name__ == "__main__":
    main()