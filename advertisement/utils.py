import speech_recognition as sr
from pydub import AudioSegment
import os
from datetime import datetime
import re


def convert_to_wav(file_path):
    audio = AudioSegment.from_file(file_path)
    wav_path = file_path.rsplit(".", 1)[0] + ".wav"
    audio.export(wav_path, format="wav")
    return wav_path

# Function to convert wav file to text (Processing in chunks)


def transcribe_audio(file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        audio_duration = source.DURATION  # Get total duration
        chunk_size = 60  # Process in 60-second chunks
        text_result = []

        for start in range(0, int(audio_duration), chunk_size):
            audio_data = recognizer.record(source, duration=chunk_size)
            try:
                text = recognizer.recognize_google(
                    audio_data, language="az-AZ")
                text_result.append(text)
            except sr.UnknownValueError:
                text_result.append("[UNRECOGNIZED]")
            except sr.RequestError as e:
                text_result.append(f"[API ERROR: {e}]")

    return " ".join(text_result)

# Function to count occurrences using regex (better accuracy)


def count_occurrences(text, search_term):
    pattern = r'\b' + re.escape(search_term.lower()) + \
        r'\b'  # Match whole word
    return len(re.findall(pattern, text.lower()))
