from typing import Dict, Any
from fastapi import UploadFile, HTTPException
import tempfile
import os

from schemas.evaluation_schema import AnalysisResponse
from core.utils import audio_tools as atools
from core.analysis.analyzer import SpeechAnalyzer
from core.transcription.transcriber import SpeechTranscriber
class AnalysisService:
    """Service to analyze an audio based on a reference audio."""
    def __init__(self):
        self.analyzer = SpeechAnalyzer()
        self.transcriber = SpeechTranscriber()
        self.tmp_audio_filepath = None
        self.base_name = None
        self.base_dir = None
        self.normalized_filepath = None
        self.normalized_filename = None

    async def _create_temporary_audio(self, audio_file: UploadFile) -> None:
        """Create a temporary .wav file in disk from the uploaded file.

        Args:
            audio_file (UploadFile): A file uploaded in a request.

        Raises:
            HTTPException: The audio file is empty.
            HTTPException: The file could not be created.
        """
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

    def _remove_temporary_audio(self) -> None:
        """Remove the temporary audio file from disk.
        """
        if self.tmp_audio_filepath and os.path.exists(self.tmp_audio_filepath):
            try:
                os.remove(self.tmp_audio_filepath)
                print(f"Temporary file removed: {self.tmp_audio_filepath}")
                
            except Exception as e:
                print(f"Error removing temporary file: {e}")
                
    def _normalize_audio(self) -> None:
        """Normalize the temporary audio file to 44100 Hz and 16 bits resolution.
        """
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

    async def analyze_audio(self, audio_file: UploadFile) -> AnalysisResponse:
        """Get the analysis of an audio file, including number of syllables,
        number of pauses, speech rate, articulation rate, speaking duration, 
        total duration, speaking to pause ratio and transcription.

        Args:
            audio_file (UploadFile): File uploaded from request.

        Raises:
            HTTPException: Error normalizing audio.

        Returns:
            AnalysisResponse: Schema for audio analysis.
        """
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
            
            return AnalysisResponse(
                number_of_syllables=audio_analysis["number_of_syllables"],
                number_of_pauses=audio_analysis["number_of_pauses"],
                speech_rate=audio_analysis["speech_rate"],
                articulation_rate=audio_analysis["articulation_rate"],
                speaking_duration=audio_analysis["speaking_duration"],
                total_duration=audio_analysis["total_duration"],
                ratio=audio_analysis["ratio"],
                transcription=audio_analysis["transcription"]
            )

        except Exception as e:
            print(f"Error analyzing file: {e}")
            raise HTTPException(status_code=500, detail="Audio analysis failed.")
        
        finally:
            self._remove_temporary_audio()

def get_analysis_service():
    return AnalysisService()
