#imports
import json
from pathlib import Path

import requests

class ImportWords:

    def __init__(self, api_direction_url:str, direction_words_jsonl:str):
       self.api_direction_url = api_direction_url
       self.direction_words_jsonl = Path(direction_words_jsonl) 

    def jsonlImport(self):
        json_words = self.direction_words_jsonl
        if json_words.exists():
            with open(json_words) as file:
                data = json.load(file)
                
                for word, content in data.items():
                    content["id"] = word
                    #print(content)
                    print(json.dumps(content, indent=4, sort_keys=True))
                    print(requests.post(self.api_direction_url, json = content))
        else:
            return "jsonl not found"
        
    