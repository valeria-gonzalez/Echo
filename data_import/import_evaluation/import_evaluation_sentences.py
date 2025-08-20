import os
import requests
import logging

class ImportEvaluationSentences:
    """
    Initialize the ImportEvaluationSentences class.

    Args:
        evaluation_api_url (str): The API endpoint used to evaluate audio files.
        audio_download_path (str): Local directory path where audio files are stored.
        evaluation_update_resources_url (str): The API endpoint used to update
        evaluation results after processing.

    Attributes:
        evaluation_api_url (str): Stores the evaluation API URL.
        audio_download_path (str): Stores the local path of downloaded audio files.
        evaluation_update_resources_url (str): Stores the update API URL for evaluations.
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
        Send evaluation results to the update evaluation API.

        Args:
            evaluation (dict): A dictionary containing audio evaluation data 
                (e.g., audio_id and audio_analysis).

        Returns:
            None

        Logs:
            - Info: The response status code from the update API.
            - Error: Any unexpected error that occurs during the request.
        """
        try:
            response = requests.put(self.evaluation_update_resources_url, json = evaluation)
            self.logger.info(f"Response evaluation api resources {response.status_code}")
        except Exception as e:
            self.logger.error(f"An error ocurred: {str(e)}")
        

    def _get_evaluation_sentences(self):
        """
        Process and evaluate audio files by sending them to the evaluation API.

        This method scans the local audio download path for `.mp3` files, 
        sends each file to the evaluation API, and processes the response. 
        The evaluation results are then sent to the update evaluation API 
        using the `_post_evaluation` method.

        Workflow:
            1. Iterate over all `.mp3` files in `self.audio_download_path`.
            2. For each file, send a POST request with the audio to `self.evaluation_api_url`.
            3. If successful, build a JSON payload with `audio_id` and `audio_analysis`.
            4. Send the payload to the update API via `_post_evaluation`.
            5. Log success or errors for each file.

        Notes:
            - Files that fail to process are stored in `fail_audios` and logged at the end.
            - Errors are caught and logged individually without interrupting the loop.

        Returns:
            None

        Raises:
            Exception: Any unexpected error during file reading or request handling is logged.
        """

        fail_audios = []
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
                            self.logger.error(response.status_code)
                        else:
                            data = {}
                            data["audio_id"] = file_name.split(".")[0]
                            data["audio_analysis"] = response.json()

                            try:
                                self._post_evaluation(data)
                                self.logger.info(f"uploaded entry successfully: {response.status_code}")
                            except Exception as e:
                                self.logger.error(f"Unexpected error with: {e}")


                except Exception as e:
                    self.logger.error(f"Unexpected error with {file_name}: {e}")
                    fail_audios.append(file_name)
        
        self.logger.info(f"Failed audios sentences {fail_audios}")