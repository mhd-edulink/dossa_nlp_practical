"""
=================================================================================================
Python script to demonstrate speech to text using SpeechRecognition package
=================================================================================================
This program converts the audio file "travel_output.wav" (that we created earlier in the speech 
to text program) to text and saves it

Process:
    1. Load the audio file (travel_output.wav)
    2. Convert the speech from the loaded output file
    3. Save the converted text into a txt file
    
Files:
    - input audio: files/travel_output.wav
    - output text: files/transcribed_speech.txt

Requirements:
    pip install SpeechRecognition

"""

# -----------------------------------------------------------------------------------------------
# 0. Import required modules
# -----------------------------------------------------------------------------------------------
import sys
from pathlib import Path

import speech_recognition as sr
import warnings

# Ignore warnings for cleaner output
warnings.filterwarnings("ignore")

# -----------------------------------------------------------------------------------------------
# 1. Define constants
# -----------------------------------------------------------------------------------------------
AUDIO_FILE: Path = Path("files/travel_output.wav")
OUTPUT_FILE: Path = Path("files/transcribed_speech.txt")

# -----------------------------------------------------------------------------------------------
# 2. Functions
# -----------------------------------------------------------------------------------------------
def load_audio(file_path: Path) -> Path:
    """
    Loads and validates the audio file from the given file path.

    Parameters:
        file_path (Path): Path to the WAV audio file.

    Returns:
        Path: The validated audio file path.

    Raises:
        FileNotFoundError: If the audio file does not exist at the specified location.
    """
    print(f"\nLoading audio file from {file_path}...")

    if not file_path.exists():
        raise FileNotFoundError(
            f"Audio file not found: {file_path}\nPlease check file location."
        )

    print("Audio file successfully loaded.")
    return file_path

def initialise_recognizer() -> sr.Recognizer:
    """
    Initialises and returns a SpeechRecognition recognizer instance.

    Returns:
        sr.Recognizer: A configured speech recognition object used for audio processing.
    """
    print("\nInitialising speech recognizer...")
    
    recognizer = sr.Recognizer()
    
    print("\nRecognizer initialised successfully.")
    return recognizer


def transcribe_audio(recognizer, audio_path: Path) -> str:
    """
    Converts speech from an audio file into text using Google's speech recognition API.

    Parameters:
        recognizer (sr.Recognizer): The speech recognition engine instance.
        audio_path (Path): Path to the WAV audio file to be transcribed.

    Returns:
        str: The transcribed text extracted from the audio file.

    Raises:
        ValueError: If the audio is unintelligible or cannot be interpreted.
        RuntimeError: If there is a failure in the speech recognition API request.
    """
    print("\nConverting speech to text...")

    with sr.AudioFile(str(audio_path)) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        print("\nTranscription successful.")
        return text

    except sr.UnknownValueError:
        raise ValueError("\nCould not transcribe audio.\nTry again or use a different audio file with clearer audio")

    except sr.RequestError as e:
        raise RuntimeError(f"API error during transcription: {e}")
    
def save_text(text: str, output_path: Path) -> None:
    """
    Saves the transcribed text into a file.

    Parameters:
        text (str): The transcribed speech text to be saved.
        output_path (Path): Path where the text file will be stored.

    Returns:
        None

    Raises:
        IOError: If the file cannot be written or saved successfully.
    """
    print(f"\nSaving transcription to {output_path}...")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    formatted_text = format_text_by_words(text)
    output_path.write_text(formatted_text, encoding="utf-8")

    if not output_path.exists():
        raise IOError("\nFailed to save transcribed text file.")

    print("\nTranscribed text saved successfully.")

# -----------------------------------------------------------------------------------------------
# 3. Helper function
# -----------------------------------------------------------------------------------------------
def print_section_heading(title: str) -> None:
    print()
    print("-" * 60)
    print(f"     {title}     ")
    print("-" * 60)
    print()
    
def format_text_by_words(text: str, words_per_line: int = 10) -> str:
    """
    Formats a string into lines containing a fixed number of words.

    Parameters:
        text (str): The input text to format.
        words_per_line (int): Number of words per line.

    Returns:
        str: Formatted multi-line string.
    """
    words = text.split()
    lines = [
        " ".join(words[i:i + words_per_line])
        for i in range(0, len(words), words_per_line)
    ]
    return "\n".join(lines)

# -----------------------------------------------------------------------------------------------
# 4. Main function
# -----------------------------------------------------------------------------------------------
def main() -> None:
    print_section_heading("SPEECH TO TEXT DEMONSTRATION")

    # Step I: Load audio file
    try:
        audio_path = load_audio(AUDIO_FILE)
    except FileNotFoundError as e:
        print(f"\nAn error occurred while loading audio file:\n{e}")
        sys.exit(1)

    # Step II: Initialise recognizer
    recognizer = initialise_recognizer()

    # Step III: Convert speech to text
    try:
        text = transcribe_audio(recognizer, audio_path)
    except (ValueError, RuntimeError) as e:
        print(f"\nAn error occurred while converting speech to text:\n{e}")
        sys.exit(1)

    # Step IV: Display result
    print_section_heading("\nTRANSCRIBED TEXT:\n")
    formatted_text = format_text_by_words(text)
    print(formatted_text)

    # Step V: Save text to file
    try:
        save_text(text, OUTPUT_FILE)
    except IOError as e:
        print(f"An error occurred while saving output text to ouput file:\n{e}")
        sys.exit(1)

    print(f"\nText saved to: {OUTPUT_FILE}")
    
    print_section_heading("MAIN METHOD END")
    
if __name__ == "__main__":
    main()