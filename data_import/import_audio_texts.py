import os
import requests

class ImportAudioTexts:
    def __init__(self, corpus_directory: str):
         self.corpus_directory = corpus_directory
          
    def _extract_chapter_directories(self)->list[str]:

            chapters = []
            
            for act_root, sub_dirs, files in os.walk(self.corpus_directory):
                if not sub_dirs:
                    chapters.append(act_root)
                    
            return chapters
    
    def _import_audio_texts(self, directory_local:str, post_directory: str):
         
        list_audios = os.listdir(directory_local)
        print(list_audios)

        for file_name in list_audios:
            print(file_name)
            file_path = os.path.join(directory_local, file_name)
            print(file_path)
            if os.path.isfile(file_path) and file_name.endswith('.flac'):
                with open(file_path, "rb") as f:

                    chapter_file_name = file_path.split("group_1_audios/")[1]
                    chapter = chapter_file_name.split("/")[0]

                    files = {"file": (file_name, f ,"audio/flac")}
                    data = {"chapter": chapter}

                    print(chapter + " este es el chapter que se manda")
                    response = requests.post(post_directory, files = files, data=data )
                    print(response)
