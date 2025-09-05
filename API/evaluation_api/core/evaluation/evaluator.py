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
        error_rate = round(wer(reference, hypothesis), 2)
        adjusted_error = round(error_rate - tolerance, 2)
        return max(0.0, adjusted_error)
    
    
    def _get_analysis_score(self, difference_analysis:dict, wer:float)->dict:
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
            "clarity": {
                "wer": 0.8, 
                "syllables": 0.2
            },
            "speed": {
                "speech_rate": 0.7,
                "speaking_duration": 0.15,
                "total_duration": 0.15
            },
            "articulation": {
                "articulation_rate": 0.8, 
                "syllables": 0.2
            },
            "rythm": {
                "ratio": 0.6,
                "pauses": 0.4
            }
        }

        def clamp(value, min_value=0, max_value=10) -> float:
            """Bounds a value in a range of min_value and max_value.
            The predifined values mean that the value is kept between a range 
            of [0,10]"""
            return max(min_value, min(value, max_value))

        # --- Clarity score ---
        wer_penalty = wer * weights["clarity"]["wer"] * 10 # Move a decimal place
        syllable_penalty = (
            abs(difference_analysis["number_of_syllables"]) * 
            weights["clarity"]["syllables"]
        ) * 10
        
        clarity_score = clamp(round(10 - (wer_penalty + syllable_penalty)))

        # --- Speed score ---
        speed_penalty = (
            abs(difference_analysis["speech_rate"]) * weights["speed"]["speech_rate"] +
            abs(difference_analysis["speaking_duration"]) * weights["speed"]["speaking_duration"] +
            abs(difference_analysis["total_duration"]) * weights["speed"]["total_duration"]
        ) * 10
        
        speed_score = clamp(round(10 - speed_penalty))

        # --- Articulation score ---
        articulation_penalty = (
            abs(difference_analysis["articulation_rate"]) * weights["articulation"]["articulation_rate"] +
            abs(difference_analysis["number_of_syllables"]) * weights["articulation"]["syllables"]
        ) * 10
        
        articulation_score = clamp(round(10 - articulation_penalty))

        # --- Rhythm score ---
        rhythm_penalty = (
            abs(difference_analysis["ratio"]) * weights["rythm"]["ratio"] +
            abs(difference_analysis["number_of_pauses"]) * weights["rythm"]["pauses"]
        ) * 10 
        
        rythm_score = clamp(round(10 - rhythm_penalty))

        # --- Total score ---
        total_score = round(
            (clarity_score + speed_score + articulation_score + rythm_score) * 100 / 40
        )

        return {
            "clarity_score": clarity_score,
            "speed_score": speed_score,
            "articulation_score": articulation_score,
            "rythm_score": rythm_score,
            "total_score": total_score
        }
        
    def get_difference_analysis(self, reference_analysis:dict, user_analysis:dict) -> dict:
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
        def relative_diff(a:float, b:float)->float:
            """Returns the difference between a and b, relative to a in a range from [0,1].
            """
            if a == 0:
                return 0 if b == 0 else 1
            return (a - b) / b
        
        categories = user_analysis.keys()
        difference_analysis = dict()
        for category in categories:
            if category != "transcription":
                difference = round(
                    relative_diff(reference_analysis[category],
                                  user_analysis[category]), 2
                )
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
        wer = self.compare_transcripts(
            reference_analysis["transcription"],
            user_analysis["transcription"]
        )
        print(f"wer: {wer}")
        difference_analysis = self.get_difference_analysis(
            reference_analysis, 
            user_analysis
        )
        print(f"difference analysis: {difference_analysis}")
        analysis_score = self._get_analysis_score(difference_analysis, wer)
        return analysis_score 