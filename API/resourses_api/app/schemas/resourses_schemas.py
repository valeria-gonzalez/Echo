from typing import List
from pydantic import BaseModel

class Definitions(BaseModel):
    pos: str
    definitions: List[str]

class Audio_analysis(BaseModel):
    number_of_syllabes: int
    number_of_pauses: int
    speech_rate: float
    articulation_rate: float
    speaking_rate: float
    speaking_duration: float
    ratio: float
    transcription: str

class sentences(BaseModel):
    audio_url: str
    text: str
    difficulty: int
    categories: List[str]
    word_count: int
    translation: str
    audio_id: int
    audio_analysis: Audio_analysis
class words(BaseModel):
    audio_url: str
    text: str
    difficulty: int
    categories: List[str]
    word_count: int
    definitions: List[Definitions]
    ipa: str
    translations: List[str]
    audio_analysis: Audio_analysis

class texts(BaseModel):
    audio_url: str
    text: str
    difficulty: int
    categories: List[str]
    word_count: int
    book_title: str
    translation: str
    audio_analysis: Audio_analysis



