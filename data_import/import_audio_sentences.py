import os
import requests

class ImportAudioSentences:
    """Imports audio files located in a directory and then posts the .mp3 file"""
    
    def __init__(self,api_direction_url_audio_sentences:str, 
                 direction_audios_download:str):
        self.api_direction_url_audio_sentences = api_direction_url_audio_sentences
        self.direction_audios_download = direction_audios_download

    def _audio_import_sentences(self):
        """Import all audio files from texts ending in .mp3"""
                
        audios_download =  self.direction_audios_download
        list_audio = os.listdir(audios_download)   

        for file_name in list_audio:
            file_path = os.path.join(audios_download,file_name)
            if os.path.isfile(file_path) and file_name.endswith('.mp3'):
                with open(file_path, "rb") as f:
                    upload_files = {"file": (file_name, f ,"audio/mpeg")}
                    response = requests.post(self.api_direction_url_audio_sentences, files = upload_files )
                    print(response)