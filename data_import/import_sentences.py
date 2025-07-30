#imports
import json
from pathlib import Path
import requests

class ImportSentences:
    
    def __init__(self, api_direction_url_sentences:str, direction_sentences_jsonl:str):
       self.api_direction_url_sentences = api_direction_url_sentences
       self.direction_sentences_jsonl = Path(direction_sentences_jsonl)

    def _tranform_json_for_db(self,json_input: dict) -> dict:
        json_db = {}

        json_db["text"] = json_input["eng_sen"]
        json_db["difficulty"] = json_input["difficulty"]
        json_db["categories"] = json_input["categories"]
        json_db["word_count"] = json_input["word_count"]
        json_db["translation"] = json_input["spa_sen"]
        json_db["audio_id"] = json_input["audio_id"]

        return json_db

    def _json_import(self):
        json_sentences = self.direction_sentences_jsonl

        if json_sentences.exists():
            with json_sentences.open() as file:
                data = json.load(file)

                for content in data:
                    sentences_json_final = self._tranform_json_for_db(content)
                    print(requests.post(self.api_direction_url_sentences, json = sentences_json_final))

        else:
            return "file not found"
        