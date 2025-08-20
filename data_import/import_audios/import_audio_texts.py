import os
import requests
import logging

class ImportAudioTexts:
    """Imports audio files located in a directory and then posts the .flac file"""
    
    def __init__(self, corpus_directory: str):
        self.corpus_directory = corpus_directory
        self.logger = logging.getLogger(self.__class__.__name__)
          
    def _extract_chapter_directories(self)->list[str]:
        """
        Collect chapter directories (leaf directories) from the corpus.

        Iterates through the directory tree starting at `self.corpus_directory` and 
        selects only directories that do not contain subdirectories (i.e., leaf nodes).

        Returns:
            list[str]: A list of paths to the chapter directories.
        """

        chapters = []
            
        for act_root, sub_dirs, files in os.walk(self.corpus_directory):
            if not sub_dirs:
                chapters.append(act_root)
                    
        return chapters
    
    def _import_audio_texts(self, 
                            directory_local:str, 
                            post_directory: str):
        
        """
        Upload `.flac` audio files from a local directory to the specified API endpoint.

        This method scans the given local directory for `.flac` files, extracts the 
        chapter information from the file path, and uploads each file along with its 
        associated metadata (`chapter`) to the provided endpoint.

        Args:
            directory_local (str): Path to the local directory containing `.flac` audio files.
            post_directory (str): API endpoint URL to which the audio files and metadata 
                will be uploaded.

        Raises:
            requests.exceptions.RequestException: If a network, timeout, or HTTP error 
                occurs during the upload process.

        Logs:
            INFO: For each successfully uploaded file with its HTTP status code.
            ERROR: If the upload of a file fails due to a request exception.
        """
         
        list_audios = os.listdir(directory_local)

        for file_name in list_audios:
            try:
                file_path = os.path.join(directory_local, file_name)
                if os.path.isfile(file_path) and file_name.endswith('.flac'):
                    with open(file_path, "rb") as f:

                        chapter_file_name = file_path.split("group_1_audios/")[1]
                        chapter = chapter_file_name.split("/")[0]

                        files = {"file": (file_name, f ,"audio/flac")}
                        data = {"chapter": chapter}

                        response = requests.post(post_directory, files = files, data=data )
                        self.logger.info(f"Uploaded: {file_name} - status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"failed to upload {file_path}: {e}")
