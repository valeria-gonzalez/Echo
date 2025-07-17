from typing import Dict, Any
from fastapi import HTTPException

from schemas.evaluation_schema import AnalysisResponse

class DatabaseService:
    """Service to analyze an audio based on a reference audio."""
    def __init__(self):
       self.API_URL = ""
       self.API_KEY = ""
       self.TABLE_NAME = ""

    async def get_reference_analysis(self, audio_id:str, type:int) -> AnalysisResponse:
        """Get the analysis of the reference audio from database. It includes
        number_of_syllables, number_of_pauses, speech_rate, 
        articulation_rate, speaking_duration, total_duration, 
        speaking_to_pause_ratio and transcription.

        Args:
            audio_id (str, optional): Reference audio id. Defaults to "".

        Returns:
            AnalysisResponse: Analysis of the reference audio.
        """
        # Get the actual analysis from firebase
        query = {
                'number_of_syllables': 6, 
                'number_of_pauses': 0, 
                'speech_rate': 2.0, 
                'articulation_rate': 2.0, 
                'speaking_duration': 5.6, 
                'total_duration': 6.0, 
                'ratio': 0.9,
                'transcription': 'life is not an exact science it is an art'
            }
        
        return AnalysisResponse(
            number_of_syllables=query["number_of_syllables"],
            number_of_pauses=query["number_of_pauses"],
            speech_rate=query["speech_rate"],
            articulation_rate=query["articulation_rate"],
            speaking_duration=query["speaking_duration"],
            total_duration=query["total_duration"],
            ratio=query["ratio"],
            transcription=query["transcription"]
        )
    

def get_database_service():
    return DatabaseService()
