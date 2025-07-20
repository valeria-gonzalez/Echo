from fastapi import APIRouter, UploadFile, Depends, HTTPException, Form
import json

from schemas.evaluation_schema import AnalysisResponse, EvaluationResponse, FeedbackResponse
from services.analysis_service import AnalysisService, get_analysis_service
from services.evaluation_service import EvaluationService, get_evaluation_service
from services.feedback_service import FeedbackService, get_feedback_service
from services.local_feedback_service import LocalFeedbackService, get_local_feedback_service

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
    reference_analysis: str = Form(...),
    user_analysis: str = Form(...),
    evaluation_service: EvaluationService = Depends(get_evaluation_service),
): 
    try:
        reference_dict = json.loads(reference_analysis)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid reference_analysis format. Must be a valid JSON."
        )
        
    try:
        user_dict = json.loads(user_analysis)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid user_analysis format. Must be a valid JSON."
        )
        
    try:
        # Call the audio evaluation service
        evaluation_response = await evaluation_service.evaluate_audio(
            reference_dict,
            user_dict
        )
        return evaluation_response
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during audio evaluation."
        )

@router.post("/feedback", response_model=FeedbackResponse)
async def feedback(
    reference_analysis: str = Form(...),
    user_analysis: str = Form(...),
    feedback_service: FeedbackService = Depends(get_feedback_service),
):      
    try:
        reference_dict = json.loads(reference_analysis)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid reference_analysis format. Must be a valid JSON."
        )
        
    try:
        user_dict = json.loads(user_analysis)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid user_analysis format. Must be a valid JSON."
        )
        
    try:
        # Call the audio feedback function
        feedback_response = await feedback_service.generate_feedback(
            user_dict,
            reference_dict
        )
        return feedback_response
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during audio feedback."
        )
        
@router.post("/feedback/local", response_model=FeedbackResponse)
async def feedback_local(
    reference_analysis: str = Form(...),
    user_analysis: str = Form(...),
    local_feedback_service: LocalFeedbackService = Depends(get_local_feedback_service),
):      
    try:
        reference_dict = json.loads(reference_analysis)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid reference_analysis format. Must be a valid JSON."
        )
        
    try:
        user_dict = json.loads(user_analysis)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid user_analysis format. Must be a valid JSON."
        )
        
    try:
        # Call the audio feedback function
        feedback_response = await local_feedback_service.generate_feedback(
            user_dict,
            reference_dict
        )
        return feedback_response
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during audio feedback."
        )
        