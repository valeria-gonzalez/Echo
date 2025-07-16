from jiwer import wer
from core.feedback.advisor import SpeechAdvisor

class SpeechEvaluator():
    """Class to evaluate speech analysis."""
    def __init__(self):
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
    
    
    def _get_analysis_score(self, user_analysis:dict, 
                       reference_analysis:dict)->dict:
        """Score the user audio analysis based on a reference audio analysis.
        The scoring will be over 10 points each and a total of 40 points.

        Args:
            user_analysis (dict): Analysis of user's audio.
            reference_analysis (dict): Analysis of reference's audio.

        Returns:
            dict: Scoring of each aspect with clarity_score, speed_score, 
            articulation_score, rythm_score, and total_score.
        """
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

        # Articulation
        articulation_ratio = safe_divide(user_analysis["articulation_rate"], reference_analysis["articulation_rate"])
        articulation_diff = abs(1 - articulation_ratio)
        articulation_score = max(0, round((1 - min(articulation_diff, 1)) * GRADING_THRESHOLD))

        # Rythm
        rythm_ratio = safe_divide(user_analysis["speaking_duration"], reference_analysis["speaking_duration"])
        rythm_diff = abs(1 - rythm_ratio)
        rythm_score = max(0, round((1 - min(rythm_diff, 1)) * GRADING_THRESHOLD))

        # Total Score
        total_score = clarity_score + speed_score + articulation_score + rythm_score
        total_score = round(total_score / TOTAL_GRADE_THRESHOLD, 2) * PERCENTAGE

        return {
            "total_score" : total_score,
            "clarity_score" : clarity_score,
            "speed_score" : speed_score,
            "articulation_score" : articulation_score,
            "rythm_score" : rythm_score
        }
        
    def _get_difference_analysis(self, user_analysis:dict, reference_analysis:dict) -> dict:
        categories = user_analysis.keys()
        difference_analysis = dict()
        for category in categories:
            if category != "transcription":
                difference = round(reference_analysis[category] - user_analysis[category], 2)
                if difference != 0:
                    difference = difference * -1
                difference_analysis[category] =  difference 
        return difference_analysis
        
    def get_score(self, user_analysis:dict, reference_analysis:dict) -> dict:
        """Get the score of the user's audio based on a reference audio.
        Both audios must be in the same directory.

        Args:
            user_audio_name (str): User audio file name.
            reference_audio_name (str): Reference audio file name.
            audio_dir (str): Audio directory.

        Returns:
            dict: User's audio score with clarity_score, speed_score, 
            articulation_score, rythm_score, and total_score.
        """
        
        analysis_score = self._get_analysis_score(user_analysis, reference_analysis)
        return analysis_score
    
    def get_feedback(self, user_analysis:dict, reference_analysis:dict) -> dict:
        """Get feedback of a user's audio based on a reference audio.
        It includes speed_tip, clarity_tip, articulation_tip, rythm_tip.

        Args:
            user_audio_name (str): User audio file name.
            reference_audio_name (str): Reference audio file name.
            audio_dir (str): Audio directory.

        Returns:
            dict: _description_
        """
        clarity = self._compare_transcripts(
            user_analysis["transcription"],
            reference_analysis["transcription"]
        )
        difference_analysis = self._get_difference_analysis(user_analysis, reference_analysis)
        
        print(reference_analysis)
        print(user_analysis)
        print(difference_analysis)
        
        feedback = self.advisor.get_feedback(difference_analysis, clarity)
        return feedback
        