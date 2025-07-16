from pydantic import BaseModel, Field
from typing import Optional, List

class AnalysisResponse(BaseModel):
    number_of_syllables: Optional[int] = Field(
        None,
        description="Overall score of the audio's speech compared to original graded over 100 percent.",
        example=30
    )
    number_of_pauses: Optional[int] = Field(
        None,
        description="Score of the clarity of the audio's speech graded over 10 points.",
        example=5
    )
    speech_rate: Optional[float] = Field(
        None,
        description="Score of the speed of the audio's speech graded over 10 points.",
        example=5
    )
    articulation_rate: Optional[float] = Field(
        None,
        description="Score of the articulation of the audio's speech graded over 10 points.",
        example=5
    )
    speaking_duration: Optional[float] = Field(
        None,
        description="Score of the rythm of the audio's speech graded over 10 points.",
        example=5
    )
    total_duration: Optional[float] = Field(
        None,
        description="Score of the rythm of the audio's speech graded over 10 points.",
        example=5
    )
    ratio: Optional[float] = Field(
        None,
        description="Score of the rythm of the audio's speech graded over 10 points.",
        example=5
    )
    transcription: Optional[str] = Field(
        None,
        description="Score of the rythm of the audio's speech graded over 10 points.",
        example=5
    )

class EvaluationResponse(BaseModel):
    total_score: Optional[int] = Field(
        None,
        description="Overall score of the audio's speech compared to original graded over 100 percent.",
        example=30
    )
    clarity_score: Optional[int] = Field(
        None,
        description="Score of the clarity of the audio's speech graded over 10 points.",
        example=5
    )
    speed_score: Optional[int] = Field(
        None,
        description="Score of the speed of the audio's speech graded over 10 points.",
        example=5
    )
    articulation_score: Optional[int] = Field(
        None,
        description="Score of the articulation of the audio's speech graded over 10 points.",
        example=5
    )
    rythm_score: Optional[int] = Field(
        None,
        description="Score of the rythm of the audio's speech graded over 10 points.",
        example=5
    )
    
class FeedbackResponse(BaseModel):
    clarity_tip: Optional[List[str]] = Field(
        None,
        description="Tips to improve clarity during speech.",
        example=["Try focusing more on vowels.", "You're overall understandable."]
    )
    speed_tip: Optional[List[str]] = Field(
        None,
        description="Tips to improve speed during speech.",
        example=["Try slowing down.", "You're speaking too fast."]
    )
    rythm_tip: Optional[List[str]] = Field(
        None,
        description="Tips to improve rythm during speech.",
        example=["Try following the original pace.", "Make note of pauses."]
    )
    articulation_tip: Optional[List[str]] = Field(
        None,
        description="Tips to improve articulation during speech.",
        example=["Focus on words with more syllables.", "Don't skip letters."]
    )
    