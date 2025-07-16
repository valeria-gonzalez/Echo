from fastapi import HTTPException
from typing import Dict, Any

from schemas.evaluation_schema import FeedbackResponse
from core.evaluation.evaluator import SpeechEvaluator
class FeedbackService():
    def __init__(self):
        self.evaluator = SpeechEvaluator()
    
    async def generate_feedback(self, audio_analysis:Dict[str, Any], 
                             reference_analysis:Dict[str,Any]) -> FeedbackResponse: 
        """Generate feedback based on an audio file and the id of the reference audio.
        It includes speed_tip, clarity_tip, articulation_tip, rythm_tip.

        Args:
            audio_file (UploadFile): File uploaded from request. 
            audio_id (str): Id of reference audio.

        Raises:
            HTTPException: Audio feedback failed.

        Returns:
            FeedbackResponse: Schema for feeback.
        """
        try:
            # Get feedback
            feedback = self.evaluator.get_feedback(audio_analysis, reference_analysis)
            
            return FeedbackResponse(
                clarity_tip = feedback["clarity_tip"],
                speed_tip = feedback["speed_tip"],
                rythm_tip=feedback["rythm_tip"],
                articulation_tip=feedback["articulation_tip"]
            )

        except Exception as e:
            print(f"Error getting feedback: {e}")
            raise HTTPException(status_code=500, detail="Audio feedback failed.")
        

def get_feedback_service():
    return FeedbackService()