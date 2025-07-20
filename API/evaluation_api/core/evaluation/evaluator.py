from jiwer import wer
class SpeechEvaluator():
    """Class to evaluate speech analysis."""
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
    
    
    def _get_analysis_score(self, user:dict, 
                       reference:dict)->dict:
        """Score the user audio analysis based on a reference audio analysis.
        The scoring will be over 10 points each and a total of 40 points.

        Args:
            user_analysis (dict): Analysis of user's audio.
            reference_analysis (dict): Analysis of reference's audio.

        Returns:
            dict: Scoring of each aspect with clarity_score, speed_score, 
            articulation_score, rythm_score, and total_score.
        """
        weights = {
            "clarity": {"wer": 0.8, "syllables": 0.2},
            "speed": {
                "speech_rate": 0.7,
                "speaking_duration": 0.15,
                "total_duration": 0.15
            },
            "articulation": {"articulation_rate": 0.8, "syllables": 0.2},
            "rythm": {
                "ratio": 0.6,
                "duration_consistency": 0.2,
                "pauses": 0.2
            }
        }

        wer = self.compare_transcripts(
            reference["transcription"],
            user["transcription"]
        )

        def clamp(value, min_value=0, max_value=10) -> float:
            return max(min_value, min(value, max_value))

        def relative_diff(a, b) -> float:
            if b == 0:
                return 0 if a == 0 else 1
            return abs(a - b) / b

        # --- Clarity score ---
        wer_penalty = wer * weights["clarity"]["wer"] * 10
        syllable_diff = relative_diff(
            user["number_of_syllables"],
            reference["number_of_syllables"]
        )
        syllable_penalty = syllable_diff * weights["clarity"]["syllables"] * 10
        clarity_score = clamp(round(10 - (wer_penalty + syllable_penalty)))

        # --- Speed score ---
        speed_penalty = (
            relative_diff(
                user["speech_rate"], 
                reference["speech_rate"]
            ) * weights["speed"]["speech_rate"] +
            relative_diff(
                user["speaking_duration"], 
                reference["speaking_duration"]
            ) * weights["speed"]["speaking_duration"] +
            relative_diff(
                user["total_duration"], 
                reference["total_duration"]
            ) * weights["speed"]["total_duration"]
        ) * 10
        speed_score = clamp(round(10 - speed_penalty))

        # --- Articulation score ---
        articulation_penalty = (
            relative_diff(
                user["articulation_rate"], 
                reference["articulation_rate"]
            ) * weights["articulation"]["articulation_rate"] +
            relative_diff(
                user["number_of_syllables"],
                reference["number_of_syllables"]
            ) * weights["articulation"]["syllables"]
        ) * 10
        articulation_score = clamp(round(10 - articulation_penalty))

        # --- Rhythm score ---
        ratio_diff = relative_diff(user["ratio"], reference["ratio"])
        duration_ratio_user = (
            user["speaking_duration"] / user["total_duration"]
            if user["total_duration"] > 0 else 0
        )
        duration_ratio_ref = (
            reference["speaking_duration"] / reference["total_duration"]
            if reference["total_duration"] > 0 else 0
        )
        duration_consistency_diff = relative_diff(
            duration_ratio_user,
            duration_ratio_ref
        )
        pause_diff = abs(user["number_of_pauses"] - reference["number_of_pauses"])

        rhythm_penalty = (
            ratio_diff * weights["rythm"]["ratio"] +
            duration_consistency_diff * weights["rythm"]["duration_consistency"]
        ) * 10 + (pause_diff * weights["rythm"]["pauses"] * 10)
        rythm_score = clamp(round(10 - rhythm_penalty))

        # --- Total score ---
        total_score = round(
            clarity_score + speed_score + articulation_score + rythm_score
        )

        return {
            "clarity_score": clarity_score,
            "speed_score": speed_score,
            "articulation_score": articulation_score,
            "rythm_score": rythm_score,
            "total_score": total_score
        }
        
    def get_difference_analysis(self, user_analysis:dict, reference_analysis:dict) -> dict:
        """Generate differences in each aspect of the analysis between the 
        user analysis and the reference analysis. 

        Args:
            user_analysis (dict): Analysis of user's audio.
            reference_analysis (dict): Analysis of reference's audio.

        Returns:
            dict: Dictionary with keys number_of_syllables, 
            number_of_pauses, rate_of_speech, articulation_rate, 
            speaking_duration, original_duration and ratio.
        """
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