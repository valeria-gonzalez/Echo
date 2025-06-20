from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from typing import Dict, Any
from schemas.evaluation_schema import FeedbackResponse, TipsResponse
from services.feedback_service import FeedbackService, get_feedback_service
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
        
@router.post("/feedback", response_model=FeedbackResponse)
async def get_pronunciation_feedback(
    audio_file: UploadFile = File(...),
    praat_service: PraatService = Depends(get_praat_service),
    feedback_service: FeedbackService = Depends(get_feedback_service)
):
    """
    Analyze audio and provide AI-generated feedback for English pronunciation.
    """
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an audio file."
        )
        
    try:
        
        praat_results = await praat_service.analyze_audio(audio_file)
        
    
        feedback_response = await feedback_service.generate_feedback(praat_results)
        
        return feedback_response
        
    except parselmouth.PraatError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Praat analysis failed: {str(e)}"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error during feedback generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during feedback generation."
        )

@router.post("/tips", response_model=TipsResponse)
async def get_pronunciation_tips(
    audio_file: UploadFile = File(...),
    praat_service: PraatService = Depends(get_praat_service),
    feedback_service: FeedbackService = Depends(get_feedback_service)
):
    """
    Analyze audio and provide personalized AI-generated tips for English 
    pronunciation improvement.
    """
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an audio file."
        )
        
    try:
        praat_results = await praat_service.analyze_audio(audio_file)
        
        tips_response = await feedback_service.generate_tips(praat_results)
        
        return tips_response
        
    except parselmouth.PraatError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Praat analysis failed: {str(e)}"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error during tips generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during tips generation."
        )