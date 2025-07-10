from jiwer import wer
from config import ARLI_API_KEY

class SpeechAdvisor:
    """Class that takes two audio analysis and returns recommendations."""
    def __init__(self):
        self.API_KEY = None
        self._load_api_key()
        
    def _load_api_key(self):
        self.API_KEY = ARLI_API_KEY
        
    def compare_transcripts(self, reference:str, hypothesis:str, 
                             tolerance:float=0.10)->float:
        """Compare two transcriptions using Word Error Rate and subtract a 
        tolerance margin.

        Args:
            reference (str): Ground truth transcription.
            hypothesis (str): Predicted transcription.
            tolerance (float): Acceptable WER threshold (e.g. 0.10 for 10%).

        Returns:
            float: Adjusted WER (WER - tolerance). If negative, the WER is within tolerance.
        """
        error_rate = wer(reference, hypothesis)
        adjusted_error = error_rate - tolerance
        return max(0.0, adjusted_error)
        