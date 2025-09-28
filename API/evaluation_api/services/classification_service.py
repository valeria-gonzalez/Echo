from fastapi import HTTPException
from typing import Dict, Any

from schemas.classification_schema import ClassificationResponse
from core.classification.classifier import SpeechClassifier
from core.evaluation.evaluator import SpeechEvaluator

class ClassificationService():
    def __init__(self):
        self.classifier = SpeechClassifier()
        self.evaluator = SpeechEvaluator()
    
    async def generate_classification(self, audio_analysis:Dict[str, Any], 
                             reference_analysis:Dict[str,Any]) -> ClassificationResponse: 
        """Generate speech performance classification based on user audio 
        analysis and reference audio analysis. Labels are Beginner, Intermediate
        and Advanced.

        Args:
            audio_analysis (Dict[str, Any]): User audio analysis.
            reference_analysis (Dict[str,Any]): Reference audio analysis.

        Raises:
            HTTPException: Audio classification failed.

        Returns:
            ClassifierResponse: Schema for classificatin.
        """
        try:
            # Get difference dictionary
            difference_analysis = self.evaluator.get_difference_analysis(
                reference_analysis,
                audio_analysis
            )
            
            # Get transcript clarity score
            clarity_score = self.evaluator.compare_transcripts(
                reference_analysis["transcription"],
                audio_analysis["transcription"]
            )
            
            classification = self.classifier.get_classification(
                difference_analysis,
                clarity_score
            )
            
            return ClassificationResponse(
                label=classification
            )

        except Exception as e:
            print(f"Error getting classification, check classification service: {e}")
            raise HTTPException(status_code=500, detail="Audio ARLI feedback failed.")
        

def get_classification_service():
    return ClassificationService()