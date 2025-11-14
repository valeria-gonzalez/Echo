from typing import Dict, Any
from fastapi import HTTPException

from schemas.evaluation_schema import EvaluationResponse
from core.evaluation.evaluator import SpeechEvaluator

class EvaluationService():
    """Service to evaluate an audio based on a reference audio."""
    def __init__(self):
        self.evaluator = SpeechEvaluator()

    async def evaluate_audio(self, audio_analysis:Dict[str, Any], 
                             reference_analysis:Dict[str,Any]) -> EvaluationResponse:
        """Generate evaluation of an audio file based on the reference audio.
        It includes total score, clarity score, speed score, articulation score
        and rythm score.

        Args:
            audio_file (UploadFile): File uploaded from request. 
            audio_id (str): Id of reference audio.

        Raises:
            HTTPException: Audio feedback failed.

        Returns:
            FeedbackResponse: Schema for feeback.
        """
        try:
            # Get final score
            score = self.evaluator.get_score(audio_analysis, reference_analysis)
            
            keys = ["total_score", "clarity_score", "speed_score", "articulation_score", "rythm_score"]
            for key in keys:
                if key not in score or score[key] is None:
                    score[key] = -1
            
            return EvaluationResponse(
                total_score=score["total_score"],
                clarity_score=score["clarity_score"],
                speed_score=score["speed_score"],
                articulation_score=score["articulation_score"],
                rythm_score=score["rythm_score"]
            )

        except Exception as e:
            print(f"Error evaluating file, check evaluation service: {e}")
            raise HTTPException(status_code=500, detail="Audio evaluation failed.")

def get_evaluation_service():
    return EvaluationService()
