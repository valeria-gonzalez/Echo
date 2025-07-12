#imports
import json
from pathlib import Path

import requests


class ImportTexts:

    def __init__(self, api_direction_url_texts:str, direction_texts_jsonl:str):
       self.api_direction_url_texts = api_direction_url_texts
       self.direction_texts_jsonl = Path(direction_texts_jsonl)

    def jsonlImport(self):
        json_text = self.direction_texts_jsonl
        if json_text.exists():
            with open(json_text) as file:
                data = json.load(file)
                for content in data:
                    print(json.dumps(content, indent=4, sort_keys=True))
                    print(requests.post(self.api_direction_url_texts, json = content))
        else:
            return "file not found"