import requests
import json
from pathlib import Path


class ImportTexts:

    def __init__(self, api_direction_url_texts:str, direction_texts_jsonl:str):
       self.api_direction_url_texts = api_direction_url_texts
       self.direction_texts_jsonl = Path(direction_texts_jsonl)

    def _trasform_json_for_db(self, input_json: dict) -> dict:

        json_db = {}
        json_db["text"] = input_json["transcript"]["full_text"]
        json_db["difficulty"] = input_json["difficulty"]
        json_db["categories"] = input_json["categories"]
        json_db["word_count"] = input_json["word_count"]
        json_db["translation"] = input_json["translation"]
        json_db["book_title"] = input_json["book_title"]

        json_db["audio_file"] = input_json["transcript"]["audio_file"]
        json_db["chapter_id"] = input_json["chapter_id"]

        return json_db
    
    def _jsonl_import(self):

        json_text = self.direction_texts_jsonl

        if json_text.exists():
            with json_text.open() as file:
                data = json.load(file)

                for content in data:
                    texts_json_final = self._trasform_json_for_db(content)
                    print(requests.post(self.api_direction_url_texts, json = texts_json_final))
        else:
            return "file not found"