import os
import requests
import logging
from mutagen.mp3 import MP3
from mutagen.flac import FLAC

class ImportAudioDuration:
    """
    ImportAudioDuration

    Class for calculating and uploading the duration of audio files for sentences, words, and texts.

    This class performs the following tasks:
    1. Initializes local directories for sentences, words, and texts audio files.
    2. Stores API endpoints to update audio durations for each type of data.
    3. Provides methods to process audio files and send their duration data to the corresponding APIs.
    4. Configures a logger to track the progress and any errors during processing.

    Attributes:
        local_directory_sentences (str): Path to the local directory containing sentence audio files.
        local_directory_words (str): Path to the local directory containing word audio files.
        local_directory_texts (str): Path to the local directory containing text audio files.
        api_resources_put_audio_duration_sentences (str): API endpoint to update sentence audio durations.
        api_resources_put_audio_duration_words (str): API endpoint to update word audio durations.
        api_resources_put_audio_duration_texts (str): API endpoint to update text audio durations.
        logger (logging.Logger): Logger instance for tracking operations and errors.
    """

    def __init__(self,
                 local_directory_sentences:str,
                 local_directory_words:str,
                 local_directory_texts:str,
                 api_resources_put_audio_duration_sentences:str,
                 api_resources_put_audio_duration_words:str,
                 api_resources_put_audio_duration_texts:str,
                 ):
        self.local_directory_sentences = local_directory_sentences
        self.local_directory_words = local_directory_words
        self.local_directory_texts = local_directory_texts
        self.api_resources_put_audio_duration_sentences = api_resources_put_audio_duration_sentences
        self.api_resources_put_audio_duration_words = api_resources_put_audio_duration_words
        self.api_resources_put_audio_duration_texts = api_resources_put_audio_duration_texts
        self.logger = logging.getLogger(self.__class__.__name__)

    def _extract_chapter_directories(self)->list[str]:
            """
            _extract_chapter_directories

            Extracts all chapter directories from the local texts audio directory.

            This method walks through the `local_directory_texts` folder and collects
            all subdirectories that do not contain further subdirectories (i.e., leaf directories),
            which correspond to individual chapters.

            Returns:
                list[str]: A list of paths to chapter directories containing audio files.
            """

            chapters = []
            
            for act_root, sub_dirs, files in os.walk(self.local_directory_texts):
                if not sub_dirs:
                    chapters.append(act_root)
                    
            return chapters
    
    def _update_audio_duration(self, 
                               data:dict, 
                               api_put_audio_duration: str):
        """
        _update_audio_duration

        Sends audio duration data to a specified API endpoint using an HTTP PUT request.

        Parameters:
            data (dict): A dictionary containing the audio duration information to be uploaded.
            api_put_audio_duration (str): The API endpoint URL where the duration data will be sent.

        Logging:
            INFO: Logs the response text returned by the API after the PUT request.
            ERROR: Logs any exceptions or errors that occur during the HTTP request.
        """


        try:
            response = requests.put(api_put_audio_duration, json = data)
            self.logger.info(f"Response api resources put audio_duration {response.text}")
        except Exception as e:
            self.logger.error(f"An error ocurred: {str(e)}")

    def _get_audio_duration_mp3(self,
                                path_file:str)-> float:
        """
        _get_audio_duration_mp3

        Calculates the duration of an MP3 audio file.

        Parameters:
            path_file (str): The full path to the MP3 file.

        Returns:
            float: Duration of the audio file in seconds. Returns 0.0 if an error occurs.

        Logging:
            ERROR: Logs the file path and exception message if the audio duration cannot be read.
        """

        try:
            audio = MP3(path_file)
            return audio.info.length
        except Exception as e:
            
            self.logger.error(f"{path_file}   {e}")
            return 0.0
        
    def _get_audio_duration_flac(self,
                                path_file:str)-> float:
        """
        _get_audio_duration_flac

        Calculates the duration of a FLAC audio file.

        Parameters:
            path_file (str): The full path to the FLAC file.

        Returns:
            float: Duration of the audio file in seconds. Returns 0.0 if an error occurs.

        Logging:
            ERROR: Logs the exception message if the audio duration cannot be read.
        """

        try:
            audio = FLAC(path_file)
            return audio.info.length
        except Exception as e:
            self.logger.error(f"{e}")
            return 0.0
        
    def _sentences(self):
        """
        _sentences

        Processes all sentence audio files in the local directory, calculates their duration,
        and uploads the duration information to the corresponding API endpoint.

        Workflow:
        1. Lists all files in the `local_directory_sentences`.
        2. Filters only MP3 files.
        3. Calculates the duration of each audio using `_get_audio_duration_mp3`.
        4. Prepares a data dictionary with `audio_id` and `audio_duration`.
        5. Sends the duration data to the API endpoint using `_update_audio_duration`.
        6. Logs success or any errors encountered during processing.

        Logging:
            INFO: Logs successful uploads of audio duration entries.
            ERROR: Logs any errors in reading files, calculating durations, or uploading data.
        """
        audios_download =  self.local_directory_sentences
        list_audio = os.listdir(audios_download)  

        for file_name in list_audio:
            path_file = os.path.join(audios_download,file_name)
            if os.path.isfile(path_file) and file_name.endswith('.mp3'):
                try:
                    response = self._get_audio_duration_mp3(path_file=path_file)

                    if(response == 0.0):
                        self.logger.error(f"Failed to read and get the audio duration")
                    else:
                        data = {}
                        data["audio_id"] = int(file_name.split(".")[0])
                        data["audio_duration"] = response

                        try:
                            self._update_audio_duration(data=data,
                                                        api_put_audio_duration=self.api_resources_put_audio_duration_sentences)
                            self.logger.info(f"uploaded entry successfully")
                        except Exception as e:
                            self.logger.error(f"Unexpected error with: {e}")


                except Exception as e:
                    self.logger.error(f"Unexpected error with {file_name}: {e}")

    def _words(self):
        """
        _words

        Processes all word audio files in the local directory, calculates their duration,
        and uploads the duration information to the corresponding API endpoint.

        Workflow:
        1. Lists all files in the `local_directory_words`.
        2. Filters only MP3 files.
        3. Calculates the duration of each audio using `_get_audio_duration_mp3`.
        4. Prepares a data dictionary with `text` (word) and `audio_duration`.
        5. Sends the duration data to the API endpoint using `_update_audio_duration`.
        6. Logs any errors encountered during processing.

        Logging:
            INFO: Logs successful uploads of audio duration entries (optional, if added).
            ERROR: Logs any errors in reading files, calculating durations, or uploading data.
        """

        audios_download =  self.local_directory_words
        list_audio = os.listdir(audios_download)  

        for file_name in list_audio:
            path_file = os.path.join(audios_download,file_name)
            if os.path.isfile(path_file) and file_name.endswith('.mp3'):
                try:
                    response = self._get_audio_duration_mp3(path_file=path_file)

                    if(response == 0.0):
                        self.logger.error(f"Failed to read and get the audio duration")
                    else:
                        data = {}
                        data["audio_duration"] = response
                        data["text"] = file_name.split(".")[0]

                        try:
                            self._update_audio_duration(data=data,
                                                        api_put_audio_duration=self.api_resources_put_audio_duration_words)
                        except Exception as e:
                            self.logger.error(f"Unexpected error with: {e}")

                except Exception as e:
                    self.logger.error(f"Unexpected error with {file_name}: {e}")

    def _put_audio_duration_texts(self, audio_download_path:str):
        """
        _put_audio_duration_texts

        Processes all text audio files in the specified directory, calculates their duration,
        and uploads the duration information to the corresponding API endpoint.

        Workflow:
        1. Lists all files in the provided `audio_download_path`.
        2. Filters only FLAC files.
        3. Extracts chapter and segment information from the file path.
        4. Only processes files named "segment_0.flac".
        5. Calculates the duration of each audio using `_get_audio_duration_flac`.
        6. Prepares a data dictionary with `audio_duration`, `chapter_id`, and `audio_file`.
        7. Sends the duration data to the API endpoint using `_update_audio_duration`.
        8. Logs success or any errors encountered during processing.

        Parameters:
            audio_download_path (str): Path to the directory containing text audio files.

        Logging:
            INFO: Logs responses or successful processing when applicable.
            ERROR: Logs any errors in reading files, calculating durations, or uploading data.
        """

        list_audios = os.listdir(audio_download_path)
        
        for file_name in list_audios:
            file_path = os.path.join(audio_download_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith('.flac'):

                chapter_file_name = file_path.split("group_1_audios/")[1]
                chapter = chapter_file_name.split("/")[0]
                segment = chapter_file_name.split("/")[1]

                if(segment == "segment_0.flac"):
                    try:
                        response = self._get_audio_duration_flac(file_path)
                        if(response != 0.0):
                            try:
                                data = {}
                                data["audio_duration"] = response
                                data["chapter_id"] = chapter
                                data["audio_file"] = segment
                                self._update_audio_duration(data=data,
                                                            api_put_audio_duration=self.api_resources_put_audio_duration_texts)
                                
                            except Exception as e:
                                self.logger.error(f"Unexpected error with: {e}")
                        else:
                            self.logger.info(f"Response API resources {response}")

                    except Exception as e:
                        self.logger.error(f"{e}")
                        
            
    def _texts(self):
        """
        _texts

        Processes all text audio files by chapter, calculates their durations,
        and uploads the duration information to the corresponding API endpoint.

        Workflow:
        1. Extracts all chapter directories using `_extract_chapter_directories`.
        2. Iterates over each chapter directory.
        3. Calls `_put_audio_duration_texts` on each directory to process FLAC audio files,
        calculate durations, and upload data to the API.

        Logging:
            INFO: Logs successful processing within `_put_audio_duration_texts`.
            ERROR: Logs any errors encountered during processing of chapter audio files.
        """

        path_list = self._extract_chapter_directories()
        for path in path_list:
            self._put_audio_duration_texts(path)
