import requests
import json
from pathlib import Path
from typing import Optional
import logging

class ImportWords:
    """
    Handles importing and uploading of word entries from a JSONL file.

    This class reads a local `.jsonl` file containing word entries with associated 
    metadata and uploads each entry to a specified API endpoint. Each word entry is 
    transformed into the expected format before being sent.

    Attributes:
        words_api_url (str): The API endpoint URL where word entries will be uploaded.
        words_jsonl_path (Path): Path to the local `.jsonl` file containing word entries.
    """
    def __init__(self, 
                 words_api_url:str, 
                 words_jsonl_path:str):
       self.words_api_url = words_api_url
       self.words_jsonl_path = Path(words_jsonl_path) 
       self.logger = logging.getLogger(self.__class__.__name__)

    def _trasform_json_for_db(self, input_json: dict) -> dict:
        """
        Transform a JSON word entry into the format expected by the database/API.

        Extracts relevant fields from the input JSON and constructs a new dictionary 
        with keys required for storage or upload, including text, difficulty, IPA 
        transcription, categories, definitions, translation, word count, and audio URL.

        Args:
            input_json (dict): Original JSON entry containing word information, 
                               including 'word', 'difficulty', 'ipa', 'categories',
                               'definitions', 'translations', and 'mp3_url'.

        Returns:
            dict: A new dictionary formatted for database insertion or API upload, 
                  containing the following keys:
                  - text (str)
                  - difficulty (str or int)
                  - word_count (int)
                  - ipa (str)
                  - categories (list)
                  - definitions (list)
                  - translation (str)
                  - audio_url (str)
        """
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

        """
        Import JSONL word entries from a local file and post each entry to the API endpoint.

        This method reads a JSONL file specified by `self.words_jsonl_path`, transforms 
        each entry using `_trasform_json_for_db`, and uploads it to the API endpoint 
        defined in `self.words_api_url`. Upload results and errors are logged.

        Logs:
            ERROR: If the JSONL file does not exist.
            INFO: For each successfully uploaded entry with the HTTP response.
            ERROR: If an upload fails due to a request exception.
            ERROR: If an unexpected exception occurs during file reading or processing.
        """

        json_words = self.words_jsonl_path
        
        if not json_words.exists():
            self.logger.error("File not found")
        
        try:
            with json_words.open() as file:
                data = json.load(file)
                
                for content in data:

                    word_json_final = self._trasform_json_for_db(content)
                    try:
                        response = requests.post(self.words_api_url, json = word_json_final)
                        self.logger.info(f"Uploaded entry successfully: {response.status_code}")
                    except requests.RequestException as e:
                        self.logger.error(f"Failed to upload entry {e}")

        except Exception as e:
            self.logger(f"An error ocurred: {str(e)}")