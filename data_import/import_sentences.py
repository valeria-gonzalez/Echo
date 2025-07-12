#imports
import json
from pathlib import Path
import requests

class ImportSentences:
    
    def __init__(self, api_direction_url_sentences:str, direction_sentences_jsonl:str):
       self.api_direction_url_sentences = api_direction_url_sentences
       self.direction_sentences_jsonl = Path(direction_sentences_jsonl)

    def jsonImport(self):
        json_sentences = self.direction_sentences_jsonl

        if json_sentences.exists():
            with open(json_sentences) as file:
                data = json.load(file)

                for content in data:
                    print(json.dumps(content, indent=4, sort_keys=True))
                    print(requests.post(self.api_direction_url_sentences, json = content))

        else:
            return "file not found"
        