import requests
import json
from pathlib import Path

class ImportWords:

    def __init__(self, api_direction_url:str, direction_words_jsonl:str):
       self.api_direction_url = api_direction_url
       self.direction_words_jsonl = Path(direction_words_jsonl) 

    def _trasform_json_for_db(self, input_json: dict) -> dict:
        json_db = {}
        json_db["text"] = input_json["word"]
        json_db["difficulty"] = input_json["difficulty"]
        json_db["word_count"] = 1
        json_db["ipa"] = input_json["ipa"]
        json_db["categories"] = input_json["categories"]
        json_db["definitions"] = input_json["definitions"]
        json_db["translation"] = input_json["translations"]
        json_db["audio_url"] = input_json["mp3_url"]

        return json_db

    def _jsonl_import(self):

        json_words = self.direction_words_jsonl
        
        if json_words.exists():
            with json_words.open() as file:
                data = json.load(file)
                
                for content in data:

                    word_json_final = self._trasform_json_for_db(content)
                    print(requests.post(self.api_direction_url, json = word_json_final))
        else:
            return "jsonl not found"
        
    