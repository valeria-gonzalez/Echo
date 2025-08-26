from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    email: str
    name: str
    password: str
    disables: bool

class User_application(BaseModel):
    user_uid: str
    last_login: datetime
    creation_date: datetime
    date_of_birth: datetime
    gender: int
    profile_picture: Optional[str] = None
    username: str

class Evaluation(BaseModel):
     audio_url: str
     total_score: int
     clarity_score: int
     speed_score: int
     articulation_score: int
     clarity_tip: str
     speed_tip:str
     rythm_tip: str
     articulation_tip:str

class AudioAnalysis(BaseModel):
    number_of_syllables: int
    number_of_pauses: int
    speech_rate: float
    articulation_rate: float
    speaking_rate: Optional[float] = None
    speaking_duration: float
    ratio: float
    transcription: str
    total_duration: Optional[float] = None

class Progress(BaseModel):
    resource_uid: str
    type: int
    completed: bool
    completion_date:datetime
    attempts: int
    last_attempt: datetime
    evaluation: Optional[Evaluation] = None
    audio_analysis: Optional[AudioAnalysis] = None

