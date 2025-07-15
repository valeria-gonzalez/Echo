from typing import Dict, Any
from fastapi import UploadFile, HTTPException
import tempfile
import os

from schemas.evaluation_schema import AnalysisResponse
from core.utils import audio_tools as atools
from core.analysis.analyzer import SpeechAnalyzer
from core.transcription.transcriber import SpeechTranscriber
from core.evaluation.evaluator import SpeechEvaluator

class AnalysisService:
    def __init__(self):
        self.analyzer = SpeechAnalyzer()
        self.transcriber = SpeechTranscriber()
        self.evaluator = SpeechEvaluator()
        self.tmp_audio_filepath = None
        self.base_name = None
        self.base_dir = None
        self.normalized_filepath = None
        self.normalized_filename = None

    async def _create_temporary_audio(self, audio_file: UploadFile):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                content = await audio_file.read()
                if not content:
                    os.remove(tmp_file.name)
                    raise HTTPException(
                        status_code=400,
                        detail="Audio file is empty."
                    )
                    
                tmp_file.write(content)
                self.tmp_audio_filepath = tmp_file.name
                self.base_name = os.path.splitext(os.path.basename(self.tmp_audio_filepath))[0]
                self.base_dir = os.path.dirname(self.tmp_audio_filepath)
                print(f"Temporary file created: {self.tmp_audio_filepath}")

        except Exception as e:
            print(f"Error creating temporary file: {e}")
            raise HTTPException(status_code=500, detail="Internal server error while handling audio file.")

    def _remove_temporary_audio(self):
        if self.tmp_audio_filepath and os.path.exists(self.tmp_audio_filepath):
            try:
                os.remove(self.tmp_audio_filepath)
                print(f"Temporary file removed: {self.tmp_audio_filepath}")
                
            except Exception as e:
                print(f"Error removing temporary file: {e}")
                
    def _normalize_audio(self):
        try:
            self.normalized_filename = atools.normalize_audio(
                audio_filename=self.base_name,
                audio_dir=self.base_dir,
                frame_rate=44100,
                resolution=2,
                overwrite=True
            )
            self.normalized_filepath = self.base_dir
            
        except Exception as e:
            print(f"Error normalizing file: {e}")
    
    def _get_source_analysis(self, audio_id:str="")->Dict[str, Any]:
        # Get the actual analysis from firebase
        temporary_analysis = {
                'number_of_syllables': 10, 
                'number_of_pauses': 0, 
                'speech_rate': 3.0, 
                'articulation_rate': 5.0, 
                'speaking_duration': 2.6, 
                'total_duration': 3.5, 
                'ratio': 0.5,
                'transcription': 'life is not an exact science it is an art'
            }
        return temporary_analysis

    async def analyze_audio(self, audio_file: UploadFile, audio_id:str) -> AnalysisResponse:
        await self._create_temporary_audio(audio_file)

        try:
            self._normalize_audio()
            # Get audio analysis
            audio_analysis = self.analyzer.get_overview(
                self.normalized_filename, 
                self.normalized_filepath
            )
            
            # Get audio transcription
            audio_analysis["transcription"] = self.transcriber.get_transcription(
                self.normalized_filename,
                self.normalized_filepath
            )
            
            # Get reference analysis
            reference_analysis = self._get_source_analysis()
            
            # Get final score
            score = self.evaluator.get_score(audio_analysis, reference_analysis)
            
            return AnalysisResponse(
                total_score=score["total_score"],
                clarity_score=score["clarity_score"],
                speed_score=score["speed_score"],
                articulation_score=score["articulation_score"],
                rythm_score=score["rythm_score"]
            )

        except Exception as e:
            print(f"Error normalizing file: {e}")
            raise HTTPException(status_code=500, detail="Audio normalization failed.")
        
        finally:
            self._remove_temporary_audio()

def get_analysis_service():
    return AnalysisService()
