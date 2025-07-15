from pydantic import BaseModel, Field
from typing import Optional

class AnalysisResponse(BaseModel):
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