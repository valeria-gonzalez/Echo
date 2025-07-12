from jiwer import wer
from analysis.analyzer import SpeechAnalyzer
from feedback.advisor import SpeechAdvisor
from transcription.transcriber import SpeechTranscriber
import utils.audio_tools as atool
class SpeechEvaluator():
    def __init__(self):
        self.analyzer = SpeechAnalyzer()
        self.transcriber = SpeechTranscriber()
        self.advisor = SpeechAdvisor()
        
    def _compare_transcripts(self, reference:str, hypothesis:str, 
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
    
    def _get_audio_analysis(self, audio_name:str, audio_dir:str)->dict:
        
        
        try:
            normalized_audio_name = atool.normalize_audio(audio_name, 
                                                          audio_dir, 
                                                          overwrite=True)
        except FileNotFoundError as e:
            print("Missing file:", e)
        except atool.AudioNormalizationError as e:
            print("Normalization error:", e)
            
        full_overview = self.analyzer.get_overview(normalized_audio_name, audio_dir)
        transcription = self.transcriber.get_transcription(normalized_audio_name, 
                                                      audio_dir)
        full_overview["transcription"] = transcription
        return full_overview
    
    
    def _get_analysis_score(self, user_analysis:dict, 
                       reference_analysis:dict)->dict:
        GRADING_THRESHOLD = 10
        TOTAL_GRADE_THRESHOLD = 40
        PERCENTAGE = 100

        def safe_divide(numerator, denominator, fallback=0.0)->float:
            return numerator / denominator if denominator != 0 else fallback

        # Clarity: Lower WER is better
        clarity = 1.0 - self._compare_transcripts(
            user_analysis["transcription"],
            reference_analysis["transcription"]
        )
        clarity_score = max(0, round(clarity * GRADING_THRESHOLD))

        # Speed
        speed_ratio = safe_divide(user_analysis["speech_rate"], reference_analysis["speech_rate"])
        speed_diff = abs(1 - speed_ratio)
        speed_score = max(0, round((1 - min(speed_diff, 1)) * GRADING_THRESHOLD))

        # Tone
        tone_ratio = safe_divide(user_analysis["articulation_rate"], reference_analysis["articulation_rate"])
        tone_diff = abs(1 - tone_ratio)
        tone_score = max(0, round((1 - min(tone_diff, 1)) * GRADING_THRESHOLD))

        # Phonetic Precision
        reference_ratio = reference_analysis["ratio"]
        user_ratio = user_analysis["ratio"]
        ratio_diff = abs(reference_ratio - user_ratio)
        phonetic_score = max(0, round((1 - min(ratio_diff, 1)) * GRADING_THRESHOLD))

        # Total Score
        total_score = clarity_score + speed_score + tone_score + phonetic_score
        total_score = round(total_score / TOTAL_GRADE_THRESHOLD, 2) * PERCENTAGE

        return {
            "total_score" : total_score,
            "clarity_score" : clarity_score,
            "speed_score" : speed_score,
            "tone_score" : tone_score,
            "phonetic_score" : phonetic_score
        }
        
    def get_analysis(self, user_audio_name:str, 
                     reference_audio_name:str, 
                     audio_dir:str) -> dict:
        reference_analysis = self._get_audio_analysis(reference_audio_name, audio_dir)
        user_analysis = self._get_audio_analysis(user_audio_name, audio_dir)
        analysis_score = self._get_analysis_score(user_analysis, 
                                                  reference_analysis)
        return analysis_score
    
    def get_feedback(self, user_audio_name:str, 
                     reference_audio_name:str, 
                     audio_dir:str):
        reference_analysis = self._get_audio_analysis(reference_audio_name, audio_dir)
        user_analysis = self._get_audio_analysis(user_audio_name, audio_dir)
        clarity = self._compare_transcripts(
            user_analysis["transcription"],
            reference_analysis["transcription"]
        )
        feedback = self.advisor.get_feedback(user_analysis, reference_analysis, clarity)
        return feedback
        