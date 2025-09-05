from fastapi import HTTPException
from typing import Dict, Any

from schemas.evaluation_schema import FeedbackResponse
from core.evaluation.evaluator import SpeechEvaluator
from core.feedback.advisor import SpeechAdvisor
class FeedbackService():
    def __init__(self):
        self.evaluator = SpeechEvaluator()
        self.advisor = SpeechAdvisor()
    
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
            # Get difference dictionary
            difference_analysis = self.evaluator.get_difference_analysis(
                audio_analysis,
                reference_analysis
            )
            
            # Get transcript clarity score
            clarity_score = self.evaluator.compare_transcripts(
                audio_analysis["transcription"],
                reference_analysis["transcription"]
            )
            
            # Get feedback
            feedback = self.advisor.get_feedback(
                difference_analysis,
                clarity_score
            )
            
            return FeedbackResponse(
                clarity_tip = feedback["clarity_tip"],
                speed_tip = feedback["speed_tip"],
                rythm_tip=feedback["rythm_tip"],
                articulation_tip=feedback["articulation_tip"]
            )

        except Exception as e:
            print(f"Error getting feedback, check feedback service: {e}")
            raise HTTPException(status_code=500, detail="Audio feedback failed.")
        

def get_feedback_service():
    return FeedbackService()