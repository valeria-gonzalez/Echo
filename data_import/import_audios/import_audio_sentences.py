import os
import requests
import logging
from pathlib import Path

class ImportAudioSentences:
    """
    Handles importing and uploading of audio sentence files.

    This class scans a local directory for `.mp3` audio files and uploads them to a 
    specified API endpoint. It is useful for automating the transfer of pre-downloaded 
    audio datasets into a remote service.

    Attributes:
        api_url (str): The API endpoint where audio files will be uploaded.
        download_dir (str): Path to the local directory containing the `.mp3` files.
    """
    
    def __init__(self,
                 api_url:str, 
                 download_dir:str):
        self.api_url = api_url
        self.download_dir = download_dir
        self.logger = logging.getLogger(self.__class__.__name__)

    def _audio_import_sentences(self):
        """
        Upload all `.mp3` audio files from the local directory to the API endpoint.

        The method scans the directory defined in `self.download_dir`, filters only `.mp3` 
        files, and attempts to upload each one to the API defined in 
        `self.api_url`. Upload results are logged with `logging`.

        Raises:
            requests.exceptions.RequestException: If an HTTP or connection error occurs 
            during the upload process.

        Logs:
            INFO: For each successfully uploaded file with its status code.
            ERROR: If a request fails due to network or server errors.
        """
                
        audios_download =  Path(self.download_dir)
        list_audio = os.listdir(audios_download)   

        for file_name in list_audio:
            try:
                file_path = os.path.join(audios_download,file_name)
                if os.path.isfile(file_path) and file_name.endswith('.mp3'):
                    with open(file_path, "rb") as f:
                        upload_files = {"file": (file_name, f ,"audio/mpeg")}
                        response = requests.post(self.api_url, files = upload_files )
                        self.logger.info(f"Uploaded: {file_name} - status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"failed to upload {file_path}: {e}")