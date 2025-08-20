import json
import os
import requests
from requests.exceptions import RequestException
import datetime
import logging

class DownloadSentences:
    """Handles downloading of sentence audio files from a JSONL dataset.

    This class reads a JSONL file containing information about sentence audio files,
    and downloads each audio file to a specified local directory.

    Attributes:
        jsonl_file (str): Path to the JSONL file containing audio metadata.
        destination_directory (str): Path to the directory where audio files will be saved.
        logger (logging.Logger): Logger instance for logging download progress and errors.
    """
 
    def __init__(self, 
                jsonl_file:str,
                destination_directory:str):
        
        self.jsonl_file = jsonl_file
        self.destination_directory = destination_directory
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def _json_download(self):
        """
        Downloads audio files listed in the JSONL file to the destination directory.

        Reads each item from the JSONL file to construct the download URL for the audio,
        and saves the audio file locally. Creates the destination directory if it does not exist.

        Logs:
            INFO: When an audio file is downloaded successfully.
            ERROR: When the download fails due to an HTTP error or network exception.

        Raises:
            requests.RequestException: If a network-related error occurs during the download.
        """
        os.makedirs(self.destination_directory, exist_ok= True)

        with open(self.jsonl_file, "r" , encoding = "utf-8") as f:
            data = json.load(f)

        for item in data:
            audio_id = item["audio_id"]
            url = f"https://tatoeba.org/audio/download/{audio_id}"
            file_name = f"{audio_id}.mp3"
            complete_path = os.path.join(self.destination_directory, file_name)
        
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    with open(complete_path, "wb") as f:
                        f.write(response.content)
                        self.logger.info(f"Audio downloaded successfully: {audio_id}")
                else:
                    self.logger.error(f"Error downloading {audio_id}. HTTP code: {response.status_code}")
            except RequestException as e:
                self.logger.error(f"Network error with audio {audio_id}: {e}")