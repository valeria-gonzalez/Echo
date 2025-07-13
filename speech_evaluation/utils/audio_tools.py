from pydub import AudioSegment
import os

class AudioNormalizationError(Exception):
    """Custom exception for audio normalization errors."""
    pass

def normalize_audio(audio_filename: str, audio_dir: str, frame_rate: int = 44100,
                    resolution: int = 2, overwrite: bool = False) -> str:
    """
    Normalize a .wav audio file to the given frame rate and resolution.

    Args:
        audio_filename (str): Filename without extension.
        audio_dir (str): Directory where the audio file is located.
        frame_rate (int, optional): Target frame rate in Hz (default: 44100).
        resolution (int, optional): Target resolution in bytes (e.g., 2 for 16-bit).
        overwrite (bool, optional): Whether to overwrite the original file.

    Returns:
        str: Path to the normalized audio file.

    Raises:
        FileNotFoundError: If the file does not exist.
        AudioNormalizationError: If the file is not a .wav file.
    """
    input_path = os.path.join(audio_dir, f"{audio_filename}.wav")

    if not input_path.lower().endswith(".wav"):
        raise AudioNormalizationError("Only .wav files are supported.")

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Audio file not found: {input_path}")

    audio = AudioSegment.from_file(input_path)

    # If already normalized
    if audio.frame_rate == frame_rate and audio.sample_width == resolution:
        return audio_filename

    # Convert
    converted = audio.set_frame_rate(frame_rate).set_sample_width(resolution)

    if overwrite:
        temp_path = input_path + ".tmp"
        converted.export(temp_path, format="wav")
        os.replace(temp_path, input_path)
        return audio_filename
    else:
        output_filename = f"{audio_filename}_converted"
        output_path = os.path.join(audio_dir, f"{output_filename}.wav")
        converted.export(output_path, format="wav")
        return output_filename
