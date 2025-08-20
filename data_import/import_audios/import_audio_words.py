import os
import requests
import logging


class ImportAudioWords:
    """
    Handles importing and uploading of word audio files.

    This class scans a local directory for `.mp3` audio files representing words 
    and uploads them to a specified API endpoint. Each file is sent along with its 
    text metadata (the filename without extension) to facilitate processing on the server.

    Attributes:
        upload_api_url (str): The API endpoint where audio files will be uploaded.
        download_dir (str): Path to the local directory containing the `.mp3` files.
    """
    
    def __init__(self,
                 upload_api_url:str, 
                 download_dir:str):
        self.upload_api_url = upload_api_url
        self.download_dir = download_dir
        self.logger = logging.getLogger(self.__class__.__name__)

    def _audio_import_words(self):
        """
        Upload `.mp3` word audio files from the local directory to the API endpoint.

        This method scans the directory defined in `self.download_dir` for `.mp3` files, 
        extracts the file name (without extension) to use as the text label, and uploads 
        each file along with its metadata to the API defined in `self.upload_api_url`.

        The results of each upload attempt are logged.

        Raises:
            requests.exceptions.RequestException: If a network, timeout, or HTTP error 
            occurs during the upload process.

        Logs:
            INFO: For each successfully uploaded file with its HTTP status code.
            ERROR: If the upload of a file fails due to a request exception.
        """
        audios_download =  self.download_dir
        list_audio = os.listdir(audios_download)   

        for file_name in list_audio:
            try:
                file_path = os.path.join(audios_download,file_name)
                if os.path.isfile(file_path) and file_name.endswith('.mp3'):
                    with open(file_path, "rb") as f:
                        upload_files = {"file": (file_name, f ,"audio/mpeg")}
                        file_within_mp3 = os.path.splitext(file_name)[0]
                        data = {"text": file_within_mp3}
                        response = requests.post(self.upload_api_url, files = upload_files, data=data )
                        self.logger.info(f"Uploaded: {file_name} - status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"failed to upload {file_name}: {e}")
