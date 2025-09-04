import os
import requests
import json
import logging

class ImportEvaluationTexts:
    """
    Initialize the ImportEvaluationTexts class.

    Args:
        local_directory (str): The parent directory containing subdirectories,
        each of which holds `.flac` audio files to be evaluated.
        evaluation_api_url (str): The API endpoint used to evaluate audio files.
        evaluation_update_resources_url (str): The API endpoint used to update
        evaluation results after processing.

    Attributes:
        local_directory (str): Stores the path of the parent directory containing audio subdirectories.
        evaluation_api_url (str): Stores the URL of the evaluation API.
        evaluation_update_resources_url (str): Stores the URL of the update API for evaluations.
    """

    def __init__(self, 
                 local_directory: str,
                 evaluation_api_url:str,
                 evaluation_update_resources_url:str):
    
        self.local_directory = local_directory
        self.evaluation_api_url = evaluation_api_url
        self.evaluation_update_resources_url = evaluation_update_resources_url
        self.logger = logging.getLogger(self.__class__.__name__)

    def _extract_chapter_directories(self)->list[str]:
            """
            Extract chapter directories from the local directory.

            This method walks through `self.local_directory` recursively 
            and collects all directories that do not contain further subdirectories. 
            These are assumed to represent chapter directories.

            Returns:
                list[str]: A list of absolute paths to chapter directories.
            """
        
            chapters = []
            
            for act_root, sub_dirs, files in os.walk(self.local_directory):
                if not sub_dirs:
                    chapters.append(act_root)
                    
            return chapters
    
    def _post_evaluation(self, evaluation:dict):
        """
        Send evaluation results to the update evaluation API.

        This method performs a PUT request to `self.evaluation_update_resources_url`
        with the provided evaluation data in JSON format. It logs the API response 
        status code upon success, or logs an error if the request fails.

        Args:
            evaluation (dict): A dictionary containing audio evaluation data 
                (e.g., audio_id, chapter_id, audio_analysis).

        Returns:
            None

        Logs:
            - Info: The response status code from the update evaluation API.
            - Error: Any unexpected error that occurs during the request.
        """
        try:
            response = requests.put(self.evaluation_update_resources_url, json = evaluation)
            self.logger.info(f"{response.status_code}")
        except Exception as e:
            self.logger.error(f"An error ocurred: {str(e)}")

        
    
    def _get_evaluation_texts(self, audio_download_path:str):
        """
        Process and evaluate `.flac` audio files corresponding to text segments.

        This method scans the given `audio_download_path` for `.flac` files, 
        extracts chapter and segment identifiers from the file path, 
        and sends selected files (`segment_0.flac`) to the evaluation API.
        The evaluation results are then sent to the update evaluation API 
        using the `_post_evaluation` method.

        Workflow:
            1. Iterate over all `.flac` files in `audio_download_path`.
            2. Extract `chapter` and `segment` information from the file path.
            3. For each `segment_0.flac`, send a POST request with the file 
               to `self.evaluation_api_url`.
            4. Build an evaluation dictionary with analysis, chapter, and audio info.
            5. Send the dictionary to `_post_evaluation`.
            6. Log failed audios and API response codes.

        Args:
            audio_download_path (str): Local directory path where `.flac` audio files are stored.

        Returns:
            None

        Logs:
            - Info: Response status codes for successful evaluations.
            - Info: List of failed audio files after processing.
            - Error: Any unexpected error during evaluation or posting.
        """
        list_audios = os.listdir(audio_download_path)
        fail_audios = []
        
        for file_name in list_audios:
            file_path = os.path.join(audio_download_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith('.flac'):
                with open(file_path, "rb") as f:

                    chapter_file_name = file_path.split("group_1_audios/")[1]
                    chapter = chapter_file_name.split("/")[0]
                    segment = chapter_file_name.split("/")[1]


                    if(segment == "segment_0.flac"):
                        files = {"audio_file": (file_name, f ,"audio/flac")}

                        response = requests.post(self.evaluation_api_url, files = files )

                        evaluation = {}
                        evaluation["audio_analysis"] = response.json()
                        evaluation["chapter_id"] = chapter
                        evaluation["audio_file"] = segment
                        
                        try:
                            self._post_evaluation(evaluation)
                            
                        except Exception as e:
                            self.logger.error(f"Unexpected error with: {e}")
                        
                        if(response.status_code != 200):
                            fail_audios.append(file_name)
                        else:
                            self.logger.info(f"Response API evaluation {response.status_code}")
        self.logger.info(f"Failed audios texts {fail_audios}")
    

