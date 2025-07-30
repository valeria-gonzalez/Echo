from typing import List, Optional
from pydantic import BaseModel

class Definitions(BaseModel):
    pos: str
    definitions: List[str]

class AudioAnalysis(BaseModel):
    number_of_syllabes: int
    number_of_pauses: int
    speech_rate: float
    articulation_rate: float
    speaking_rate: float
    speaking_duration: float
    ratio: float
    transcription: str

class sentences(BaseModel):
    audio_url: Optional[str] = None
    text: str
    difficulty: int
    categories: List[str]
    word_count: int
    translation: str
    audio_id: int
    audio_analysis: Optional[AudioAnalysis] = None
class words(BaseModel):
    audio_url: Optional[str] = None
    text: str
    difficulty: int
    categories: List[str]
    word_count: int
    definitions: List[Definitions]
    ipa: str
    translation: List[str]
    audio_analysis: Optional[AudioAnalysis] = None

class texts(BaseModel):
    audio_url: Optional[str] = None
    text: str
    difficulty: int
    categories: List[str]
    word_count: int
    book_title: str
    translation: str
    audio_analysis: Optional[AudioAnalysis] = None

    chapter_id: str
    audio_file:str

class SentencesEvaluation(BaseModel):
    audio_id: int
    audio_analysis: AudioAnalysis

class TextsEvaluation(BaseModel):
    chapter_id: str
    audio_file: str
    audio_analysis: AudioAnalysis



