#imports
import json
from pathlib import Path
import requests
from typing import Optional

class ImportSentences:
    """tranforms the jsonl sentences to have the same 
    fiels as the db and imports the json"""
    def __init__(self, api_direction_url_sentences:str, direction_sentences_jsonl:str):
       self.api_direction_url_sentences = api_direction_url_sentences
       self.direction_sentences_jsonl = Path(direction_sentences_jsonl)

    def _tranform_json_for_db(self,json_input: dict) -> dict:

        """tranforms a JSON in the format expected by the database
        
        Args: 
            input_json(dict): Original dictionary 

        Returns:
            dict: JSON with keys matching the database schema """
        
        json_db = {}

        json_db["text"] = json_input["eng_sen"]
        json_db["difficulty"] = json_input["difficulty"]
        json_db["categories"] = json_input["categories"]
        json_db["word_count"] = json_input["word_count"]
        json_db["translation"] = json_input["spa_sen"]
        json_db["audio_id"] = json_input["audio_id"]

        return json_db

    def _json_import(self) -> Optional[str]:
        """Reads the JSONL file and post each iteam to the API
        
        Returns: 
            Optional[str]: error message
            otherwise, returns none
        """
        json_sentences = self.direction_sentences_jsonl

        if not json_sentences.exists():
            return "File not found"
        
        try:
            with json_sentences.open() as file:
                data = json.load(file)

                for content in data:
                    sentences_json_final = self._tranform_json_for_db(content)
                    print(requests.post(self.api_direction_url_sentences, json = sentences_json_final))

        except Exception as e:
            return f"An error ocurred: {str(e)}"
        