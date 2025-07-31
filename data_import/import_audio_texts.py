import os
import requests

class ImportAudioTexts:
    """Imports audio files located in a directory and then posts the .flac file"""
    
    def __init__(self, corpus_directory: str):
         self.corpus_directory = corpus_directory
          
    def _extract_chapter_directories(self)->list[str]:
            """gets all directories within a directory

            returns: 
                list[str]: return a list of directories
            """
        
            chapters = []
            
            for act_root, sub_dirs, files in os.walk(self.corpus_directory):
                if not sub_dirs:
                    chapters.append(act_root)
                    
            return chapters
    
    def _import_audio_texts(self, directory_local:str, post_directory: str):
        """Import all audio files from texts ending in .flac
         
        Args:
        directory_local as string: is the location where all the directories 
        containing the audio files to be imported are located.

        post_directory as string: It is the address of the endpoint to which
         the audio will be sent.

        Return:
            none
        """
         
        list_audios = os.listdir(directory_local)

        for file_name in list_audios:
            file_path = os.path.join(directory_local, file_name)
            if os.path.isfile(file_path) and file_name.endswith('.flac'):
                with open(file_path, "rb") as f:

                    chapter_file_name = file_path.split("group_1_audios/")[1]
                    chapter = chapter_file_name.split("/")[0]

                    files = {"file": (file_name, f ,"audio/flac")}
                    data = {"chapter": chapter}

                    response = requests.post(post_directory, files = files, data=data )
                    print(response)
