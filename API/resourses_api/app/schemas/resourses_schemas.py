from typing import List
from pydantic import BaseModel


class Transcript(BaseModel):
    audio_file: str
    duration: float
    full_text: str
    text_lines: List[str]

class texts(BaseModel):
    #id: str
    #text_id: int
    chapter_id: str
    book_title: str

    transcript: Transcript

    difficulty: int
    categories: List[str]
    #word_count: int

class DefinitionsIn(BaseModel):
    pos: str
    definitions: List[str]

class words(BaseModel):
    #id: str
    word: str
    definitions: List[DefinitionsIn]
    ipa: str
    mp3_url: str
    translations: list[str]
    categories: list[str]
    difficulty: int

class sentences(BaseModel):
    #id: int
    #sentences_id: int
    eng_sen: str
    spa_sen: str
    audio_id: int
    #duration: int
    categories: List[str]
    difficulty: int