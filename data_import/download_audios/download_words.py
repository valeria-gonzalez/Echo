import json
import os
import requests
import time
import logging

class DownloadWords:
    """Handles downloading of word audio files from a JSONL dataset.

    This class reads a JSONL file containing information about word audio files
    and provides functionality to download each audio file to a specified local directory.

    Attributes:
        jsonl_file (str): Path to the JSONL file containing audio metadata.
        destination_directory (str): Directory where audio files will be saved.
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
        Downloads audio files listed in a JSONL file to the destination directory.

        Reads each item from the JSONL file specified by `self.jsonl_file`, constructs
        the audio URL from the "mp3_url" field, and saves each audio file using the
        "word" field as the filename. Creates the destination directory if it does not exist.

        The method adds a short delay between requests to avoid overloading the server.

        Logs:
            INFO: When an audio file is downloaded successfully along with the HTTP status code.
            ERROR: When the download fails due to an HTTP error or a network exception.

        Raises:
            requests.exceptions.RequestException: If a network-related error occurs during a download.
        """
        
        os.makedirs(self.destination_directory, exist_ok= True)

        with open(self.jsonl_file, "r" , encoding = "utf-8") as f:
            data = json.load(f)

        for item in data:
            audio_name = item.get("word")
            audio_url = item.get("mp3_url")
            url = f"{audio_url}"
            file_name = f"{audio_name}.mp3"
            complete_path = os.path.join(self.destination_directory, file_name)

            try:
                response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x84_64)"}, timeout=10)

                if response.status_code == 200:
                    with open(complete_path, "wb") as f:
                        f.write(response.content)
                        self.logger.info(f" {response.status_code} - downloaded: {audio_name}")
                else:
                    self.logger.error(f"Error {response.status_code} with audio {audio_name}")

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed for {audio_name}: {e}")

            time.sleep(0.1)
