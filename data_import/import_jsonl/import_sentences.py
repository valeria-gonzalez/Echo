#imports
import json
from pathlib import Path
import requests
import logging

class ImportSentences:
    """
    Handles importing and uploading of sentence entries from a JSONL file.

    This class reads a local `.jsonl` file containing sentence entries with 
    associated metadata and uploads each entry to a specified API endpoint. 
    Each sentence entry is transformed into the expected format before being sent.

    Attributes:
        sentences_api_url (str): The API endpoint URL where sentence entries will be uploaded.
        sentences_jsonl_path (Path): Path to the local `.jsonl` file containing sentence entries.
    """
    def __init__(self, 
                 sentences_api_url:str, 
                 sentences_jsonl_path:str):
       self.sentences_api_url = sentences_api_url
       self.sentences_jsonl_path = Path(sentences_jsonl_path)
       self.logger = logging.getLogger(self.__class__.__name__)

    def _tranform_json_for_db(self,json_input: dict) -> dict:
        """
        Transform a JSON sentence entry into the format expected by the database/API.

        Extracts relevant fields from the input JSON and constructs a new dictionary 
        with keys required for storage or upload, including text, difficulty, categories, 
        word count, translation, and audio ID.

        Args:
            json_input (dict): Original JSON entry containing sentence information, 
                               including 'eng_sen', 'difficulty', 'categories', 
                               'word_count', 'spa_sen', and 'audio_id'.

        Returns:
            dict: A new dictionary formatted for database insertion or API upload, 
                  containing the following keys:
                  - text (str)
                  - difficulty (str or int)
                  - categories (list)
                  - word_count (int)
                  - translation (str)
                  - audio_id (str)
        """

        
        json_db = {}

        json_db["text"] = json_input["eng_sen"]
        json_db["difficulty"] = json_input["difficulty"]
        json_db["categories"] = json_input["categories"]
        json_db["word_count"] = json_input["word_count"]
        json_db["translation"] = json_input["spa_sen"]
        json_db["audio_id"] = json_input["audio_id"]

        return json_db

    def _json_import(self):
        """
        Import JSON sentence entries from a local file and post each entry to the API endpoint.

        This method reads a JSONL file specified by `self.sentences_jsonl_path`, transforms 
        each entry using `_tranform_json_for_db`, and uploads it to the API endpoint 
        defined in `self.sentences_api_url`. Upload results and errors are logged.

        Logs:
            ERROR: If the JSONL file does not exist.
            INFO: For each successfully uploaded entry with its HTTP status code.
            ERROR: If an upload fails due to a request exception.
            ERROR: If an unexpected exception occurs during file reading or processing.
        """
        json_sentences = self.sentences_jsonl_path

        if not json_sentences.exists():
            self.logger.error( "File not found")
        
        try:
            with json_sentences.open() as file:
                data = json.load(file)


                for content in data:
                    sentences_json_final = self._tranform_json_for_db(content)
                    try:
                        response = requests.post(self.sentences_api_url, json = sentences_json_final)
                        self.logger.info(f"Uploaded entry successfully: {response.status_code}")
                    except requests.RequestException as e:
                        self.logger.error(f"Failed to upload entry {e}")

        except Exception as e:
            self.logger(f"An error ocurred: {str(e)}")
        