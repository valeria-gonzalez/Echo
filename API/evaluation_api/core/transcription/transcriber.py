import whisper
import warnings
import string
import os

class SpeechTranscriber:
    """Class for the transcription of audios."""
    def __init__(self, model_size: str = "small.en"):
        self.model = None
        self.model_size = model_size
        self._load_model()
        
    def _load_model(self):
        """Load small Open AI Whisper model for english transcriptions"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            self.model = whisper.load_model("small.en")
        
    def get_transcription(self, audio_filename: str, audio_dir: str) -> str:
        """Transcribe the given audio file to text.

        Args:
            audio_filename (str): Filename without extension.
            audio_dir (str): Filepath where the audio is.
            suppress_punctuation (bool): Whether to suppress punctuation marks in output.

        Returns:
            str: Clean transcription of the audio file.
        """
        full_audio_path = os.path.join(audio_dir, f"{audio_filename}.wav")

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            result = self.model.transcribe(full_audio_path)
            transcription = result["text"]
            clean_transcription = transcription.translate(
                str.maketrans('', '', string.punctuation)
            )

        return clean_transcription.strip().lower()