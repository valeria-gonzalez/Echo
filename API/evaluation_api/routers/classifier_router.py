from fastapi import APIRouter, Depends, HTTPException, Form
import json

from schemas.classification_schema import ClassificationResponse
from services.classification_service import ClassificationService, get_classification_service

router_classification = APIRouter(
    prefix="/classification",
    tags=["Audio Classification"],
)

@router_classification.get("/")
async def root():
    return {"message": "Welcome to the Audio Clasification API prefix!"}

@router_classification.post("/classify_audio", response_model=ClassificationResponse)
async def classify_audio(
    reference_analysis: str = Form(...),
    user_analysis: str = Form(...),
    classification_service: ClassificationService = Depends(get_classification_service),
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
        # Call the audio classification service
        classification_response = await classification_service.generate_classification(
            user_dict,
            reference_dict,
        )
        return classification_response
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during audio classification."
        )
