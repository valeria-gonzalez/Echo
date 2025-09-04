import requests
import json
from pathlib import Path
from typing import Optional
import logging



class ImportTexts:
    """
    Handles importing and uploading of text entries from a JSONL file.

    This class reads a local `.jsonl` file containing text entries with associated 
    metadata and uploads each entry to a specified API endpoint. It is useful for 
    automating the ingestion of textual datasets into a remote service.

    Attributes:
        texts_api_url (str): The API endpoint URL where text entries will be uploaded.
        texts_jsonl_path (Path): Path to the local `.jsonl` file containing text entries.
    """
    def __init__(self, 
                 texts_api_url:str, 
                 texts_jsonl_path:str):
       
       self.texts_api_url = texts_api_url
       self.texts_jsonl_path = Path(texts_jsonl_path)
       self.logger = logging.getLogger(self.__class__.__name__)

    def _trasform_json_for_db(self, input_json: dict) -> dict:
        """
        Transform a JSON entry into the format expected by the database/API.

        Extracts relevant fields from the input JSON and constructs a new dictionary 
        with keys required for storage or upload, including text, difficulty, categories, 
        word count, translation, book title, audio file, and chapter ID.

        Args:
            input_json (dict): Original JSON entry containing transcript, metadata, 
                               and chapter information.

        Returns:
            dict: A new dictionary formatted for database insertion or API upload, 
                  containing the following keys:
                  - text (str)
                  - difficulty (str or int)
                  - categories (list)
                  - word_count (int)
                  - translation (str)
                  - book_title (str)
                  - audio_file (str)
                  - chapter_id (str or int)
        """
        
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
        """
        Import JSONL data from a local file and post each entry to the API endpoint.

        This method reads a JSONL file specified by `self.direction_texts_jsonl`, 
        transforms each entry using `_trasform_json_for_db`, and uploads it to the API 
        endpoint `self.api_direction_url_texts`. Upload results and errors are logged.

        Logs:
            ERROR: If the JSONL file does not exist.
            INFO: For each successfully uploaded entry with its HTTP status code.
            ERROR: If an upload fails due to a request exception.
            ERROR: If an unexpected exception occurs during file reading or processing.
        """
        
        json_file = self.texts_jsonl_path

        if not json_file.exists():
            self.logger.error("File not found")
        
        try:

            with json_file.open() as file:
                data = json.load(file)

                for content in data:
                    texts_json_final = self._trasform_json_for_db(content)
                    try:
                        response = requests.post(self.texts_api_url, json = texts_json_final)
                        self.logger.info(f"Uploaded entry successfully: {response.status_code}")
                    except requests.RequestException as e:
                        self.logger.error(f"Failed to upload entry: {e}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}") 