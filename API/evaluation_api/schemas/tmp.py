from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class PraatAnalysisResponse(BaseModel):
    pitch_mean_hz: Optional[float] = Field(
        None,
        description="Mean pitch frequency in Hertz.",
        example=120.55
    )
    intensity_mean_db: Optional[float] = Field(
        None,
        description="Mean intensity in decibels.",
        example=65.60
    )
    jitter_local_percent: Optional[float] = Field(
        None,
        description="Local jitter in percentage.",
        example=0.1534
    )
    shimmer_local_db: Optional[float] = Field(
        None,
        description="Local shimmer in decibels.",
        example=0.1234
    )
    f1_mid_hz: Optional[float] = Field(
        None,
        description="Mid F1 frequency in Hertz.",
        example=500.0
    )
    f2_mid_hz: Optional[float] = Field(
        None,
        description="Mid F2 frequency in Hertz.",
        example=1500.0
    )
    duration_s: Optional[float] = Field(
        None,
        description="Duration of the audio in seconds.",
        example=3.5
    )
    message: str = Field(
        ...,
        description="Message indicating the result of the analysis.",
        example="Audio analysis completed successfully."
    )

class FeedbackResponse(BaseModel):
    overall_score: float = Field(
        ...,
        description="Overall pronunciation score from 0 to 10",
        example=7.5,
        ge=0,
        le=10
    )
    detailed_feedback: str = Field(
        ...,
        description="Detailed AI-generated feedback about the pronunciation",
        example=f"Your English pronunciation shows good volume control and "
        f"natural pitch range. However, there is some pitch instability that " 
        f"could be improved with practice."
    )
    vocal_characteristics: Dict[str, str] = Field(
        ...,
        description="Interpreted vocal characteristics",
        example={
            "pitch": "Normal pitch range, very natural",
            "intensity": "Good volume range, clear and natural",
            "jitter": "Moderate pitch variation, slightly rough",
            "shimmer": "Good volume stability, smooth delivery"
        }
    )
    recommendations: List[str] = Field(
        ...,
        description="AI-generated specific recommendations for improvement",
        example=[
            "Practice sustained vowel sounds to improve pitch stability",
            "Work on breath support for steadier voice production",
            "Focus on consistent airflow during speech"
        ]
    )
    praat_data: PraatAnalysisResponse = Field(
        ...,
        description="Original Praat analysis data"
    )

class TipsResponse(BaseModel):
    personalized_tips: List[str] = Field(
        ...,
        description="AI-generated personalized pronunciation tips",
        example=[
            "Practice humming English melodies to improve pitch control",
            "Breathe from your diaphragm, not your chest",
            "Imagine you're speaking to someone across the room"
        ]
    )
    exercises: List[str] = Field(
        ...,
        description="AI-generated specific practice exercises",
        example=[
            "Sustain 'ahh' sound for 15 seconds with steady pitch",
            "Count from 1 to 20 maintaining consistent volume",
            "Practice reading news articles aloud with good projection"
        ]
    )
    focus_areas: List[str] = Field(
        ...,
        description="Identified areas that need focused attention",
        example=["Pitch stability", "Volume control", "Voice projection"]
    )
    difficulty_level: str = Field(
        ...,
        description="Recommended difficulty level for practice",
        example="Intermediate - Improvement"
    )
    praat_data: PraatAnalysisResponse = Field(
        ...,
        description="Original Praat analysis data"
    )