from pydantic import BaseModel, Field
from typing import Optional

class PraatAnalysisResultSchema(BaseModel):
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