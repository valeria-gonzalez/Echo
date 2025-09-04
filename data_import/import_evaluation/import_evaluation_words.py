import os
import requests
import json
import logging

class ImportEvaluationWords:
    """
    Handles the evaluation of word audio files by interacting with a remote API.

    Attributes:
        evaluation_api_url (str): URL of the API used to perform evaluations.
        audio_download_path (str): Local path where audio files to be evaluated are stored.
        evaluation_update_resources_url (str): URL of the API endpoint to update evaluation results.
    """
    def __init__(self,
                 evaluation_api_url:str, 
                 audio_download_path:str,
                 evaluation_update_resources_url:str):
        self.evaluation_api_url = evaluation_api_url
        self.audio_download_path = audio_download_path
        self.evaluation_update_resources_url = evaluation_update_resources_url
        self.logger = logging.getLogger(self.__class__.__name__)

    def _post_evaluation(self, evaluation:dict):
        """
        Sends an evaluation to the resource update endpoint using a PUT request.

        Args:
            evaluation (dict): Dictionary containing the evaluation data to be sent to the server.

        Logs:
            - INFO: Status code of the server response.
            - ERROR: Error message if an exception occurs during the request.
        """
        try:
            response = requests.put(self.evaluation_update_resources_url, json = evaluation)
            self.logger.info("request API resources " + response.status_code)

        except Exception as e:
            self.logger.error(f"An error ocurred: {str(e)}")
    
    def _get_evaluation_words(self):
        """
        Process and evaluate `.mp3` audio files corresponding to single words.

        This method scans the local audio download path for `.mp3` files, 
        sends each file to the evaluation API, and processes the response. 
        The evaluation results are then sent to the update resources API 
        using the `_post_evaluation` method.

        Workflow:
            1. Iterate over all `.mp3` files in `self.audio_download_path`.
            2. Send each file to `self.evaluation_api_url` via a POST request.
            3. If the response is successful, build a dictionary containing
               `text` (from the filename) and `audio_analysis`.
            4. Send the dictionary to `_post_evaluation`.
            5. Log errors for failed uploads or unexpected exceptions.

        Args:
            None

        Returns:
            None

        Logs:
            - Info: Response status codes for successful evaluations.
            - Error: Any unexpected error during file reading, request, or posting.
        """
                
        audios_download =  self.audio_download_path
        list_audio = os.listdir(audios_download)   

        for file_name in list_audio:
            file_path = os.path.join(audios_download,file_name)
            if os.path.isfile(file_path) and file_name.endswith('.mp3'):
                try:
                    with open(file_path, "rb") as f:

                        upload_files = {"audio_file": (file_name, f ,"audio/mpeg")}
                        response = requests.post(self.evaluation_api_url, files = upload_files )

                        if(response.status_code != 200):
                            self.logger.info("response API evaluation" + response.status_code)
                        else:
                            data = {}
                            data["audio_analysis"] = response.json()
                            data["text"] = file_name.split(".")[0]

                            try:
                                self._post_evaluation(data)
                                
                                
                            except Exception as e:
                                self.logger.error(f"Unexpected error with: {e}")

                except Exception as e:
                    self.logger.error(f"Unexpected error with {file_name}: {e}")
