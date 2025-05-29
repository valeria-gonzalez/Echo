from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from typing import Dict, Any

from services.praat_service import PraatService, get_praat_service
import parselmouth

router = APIRouter(
    prefix="/evaluation",
    tags=["Audio Evaluation"],
)

@router.post("/analyze_audio", response_model=Dict[str, Any])
async def analyze_audio(
    audio_file: UploadFile = File(...),
    praat_service: PraatService = Depends(get_praat_service)
):
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an audio file."
        )
        
    try:
        analysis_results = await praat_service.analyze_audio(audio_file)
        return analysis_results
    except parselmouth.PraatError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Praat analysis failed: {str(e)}"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during audio analysis."
        )