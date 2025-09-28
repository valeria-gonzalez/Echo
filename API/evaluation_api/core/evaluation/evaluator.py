from jiwer import wer
import math
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
        error_rate = round(wer(reference, hypothesis), 1)
        adjusted_error = max(0.0, round(error_rate - tolerance, 1))
        print(f"wer:{adjusted_error}")
        print(f"Calculating wer...success!")
        return adjusted_error
    
    
    def _get_analysis_score(self, difference_analysis: dict, wer: float) -> dict:
        """Score the user audio analysis based on a reference audio analysis.
        Each category is over 10 points, total over 100 points.

        Args:
            difference_analysis (dict): Relative difference between reference and user analysis.
            wer (float): Word Error Rate.

        Returns:
            dict: Integer scores for clarity, speed, articulation, rythm, and total_score.
        """
        
        weights = {
            "clarity": {"wer": 0.9, "syllables": 0.1},
            "speed": {
                "speech_rate": 0.7, 
                "speaking_duration": 0.15, 
                "total_duration": 0.15
            },
            "articulation": {"articulation_rate": 0.8, "syllables": 0.2},
            "rythm": {"ratio": 0.7, "pauses": 0.3},
        }

        def compute_score(criteria_weight: dict) -> int:
            """Compute a weighted integer score (0-10) for an assessment 
            criteria given each of the weighted metrics."""
            score = 0
            for metric, weight in criteria_weight.items():
                if metric == "wer":
                    diff = wer
                else:
                    diff = abs(difference_analysis.get(metric, 0))
                diff = min(diff, 1)  # cap at 1 so next step isn't negative
                metric_score = (1 - diff) * weight
                score += metric_score
            return max(0, min(10, round(score * 10)))  # scale to 10

        clarity_score = compute_score(weights["clarity"])
        speed_score = compute_score(weights["speed"])
        articulation_score = compute_score(weights["articulation"])
        rythm_score = compute_score(weights["rythm"])

        # Multiply by 2.5 because each category is 25 out of 100
        total_score = round(
            (clarity_score + speed_score + articulation_score + rythm_score) * 2.5
        )
        
        print(f"Calculating evaluation score...success!")
        return {
            "clarity_score": clarity_score,
            "speed_score": speed_score,
            "articulation_score": articulation_score,
            "rythm_score": rythm_score,
            "total_score": total_score,
        }
        
    def get_difference_analysis(self, reference_analysis:dict, user_analysis:dict) -> dict:
        """Generate relative differences for each metric between the 
        user analysis and the reference analysis. Each difference has a value
        between (0,1). Results closer to 0 mean similarity and closer to 1 mean dissimilarity.
        Positive values mean more of a metric and negative less of a value.

        Args:
            user_analysis (dict): Analysis of user's audio.
            reference_analysis (dict): Analysis of reference's audio.

        Returns:
            dict: Dictionary with keys number_of_syllables, 
            number_of_pauses, rate_of_speech, articulation_rate, 
            speaking_duration, original_duration and ratio.
        """
        def relative_diff(a: float, b: float) -> float:
            """Returns how dissimilar b is in reference to a.
            0 means identical, 1 means maximally dissimilar.
            """
            if a == 0:
                return 0.0 if b == 0 else 1.0
            return min(1.0, abs(a - b) / abs(a))
        
        categories = user_analysis.keys()
        difference_analysis = dict()
        for category in categories:
            if category != "transcription":
                difference = math.trunc(
                    relative_diff(reference_analysis[category],
                                  user_analysis[category]) * 10
                ) / 10
                if user_analysis[category] < reference_analysis[category]:
                    difference *= -1
                difference_analysis[category] =  difference
        
        print("difference analysis:")
        for key, value in difference_analysis.items():
            print(f"{key}: {value}")
            
        print(f"Calculating difference analysis...success!") 
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
        difference_analysis = self.get_difference_analysis(
            reference_analysis, 
            user_analysis
        )
        analysis_score = self._get_analysis_score(difference_analysis, wer)
        return analysis_score 