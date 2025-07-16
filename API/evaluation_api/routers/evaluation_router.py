from fastapi import APIRouter, UploadFile, Depends, HTTPException, Form
from typing import Dict, Any

from schemas.evaluation_schema import AnalysisResponse, EvaluationResponse, FeedbackResponse
from services.analysis_service import AnalysisService, get_analysis_service
from services.evaluation_service import EvaluationService, get_evaluation_service
from services.feedback_service import FeedbackService, get_feedback_service
from services.database_service import DatabaseService, get_database_service

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
    analysis_service: AnalysisService = Depends(get_analysis_service)
): 
    # Make sure an audio file was passed
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an audio file."
        )
        
    try:
        # Call the audio analysis service
        analysis_response = await analysis_service.analyze_audio(audio_file)
        return analysis_response
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during audio analysis."
        )

@router.post("/evaluate_audio", response_model=EvaluationResponse)
async def evaluate_audio(
    audio_file: UploadFile,
    audio_id: str = Form(...),
    resource_type:int = Form(...),
    evaluation_service: EvaluationService = Depends(get_evaluation_service),
    analysis_service: AnalysisService = Depends(get_analysis_service),
    database_service:DatabaseService = Depends(get_database_service)
): 
    # Make sure an audio file was passed
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an audio file."
        )
        
    try:
        # Get audio analysis
        audio_analysis = await analysis_service.analyze_audio(audio_file)
        
        # Get reference analysis
        reference_analysis = await database_service.get_reference_analysis(audio_id,
                                                                           resource_type)
        
        # Call the audio evaluation service
        evaluation_response = await evaluation_service.evaluate_audio(audio_analysis.model_dump(),
                                                                      reference_analysis.model_dump())
        
        return evaluation_response
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during audio evaluation."
        )


@router.post("/feedback", response_model=FeedbackResponse)
async def feedback(
    audio_file: UploadFile,
    audio_id: str = Form(...),
    resource_type:int = Form(...),
    feedback_service: FeedbackService = Depends(get_feedback_service),
    analysis_service: AnalysisService = Depends(get_analysis_service),
    database_service:DatabaseService = Depends(get_database_service)
): 
    # Make sure an audio file was passed
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an audio file."
        )
        
    try:
        # Get audio analysis
        audio_analysis = await analysis_service.analyze_audio(audio_file)
        
        # Get reference analysis
        reference_analysis = await database_service.get_reference_analysis(audio_id,
                                                                           resource_type)
        
        # Call the audio feedback function
        feedback_response = await feedback_service.generate_feedback(audio_analysis.model_dump(),
                                                                     reference_analysis.model_dump())
        
        return feedback_response
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during audio feedback."
        )
        