from fastapi import APIRouter, UploadFile, Depends, HTTPException, Form
from typing import Dict, Any
from schemas.evaluation_schema import AnalysisResponse, FeedbackResponse
from services.analysis_service import AnalysisService, get_analysis_service

router = APIRouter(
    prefix="/evaluation",
    tags=["Audio Evaluation"],
)

@router.get("/")
async def root():
    return {"message": "Welcome to the Audio Evaluation API prefix!"}

@router.post("/analyze_audio", response_model=AnalysisResponse)
async def analyze_audio(
    audio_file: UploadFile,
    audio_id: str = Form(...),
    analysis_service: AnalysisService = Depends(get_analysis_service)
): 
    # Make sure an audio file was passed
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an audio file."
        )
        
    try:
        # Call the audio analysis function
        analysis_results = await analysis_service.analyze_audio(audio_file, audio_id)
        return analysis_results
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during audio analysis."
        )
        
@router.post("/feedback", response_model=FeedbackResponse)
async def analyze_audio(
    audio_file: UploadFile,
    audio_id: str = Form(...),
    analysis_service: AnalysisService = Depends(get_analysis_service)
): 
    # Make sure an audio file was passed
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an audio file."
        )
        
    try:
        # Call the audio analysis function
        analysis_results = await analysis_service.analyze_audio(audio_file, audio_id)
        return analysis_results
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during audio analysis."
        )