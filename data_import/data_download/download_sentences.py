import json
import os
import requests
import datetime

class DownloadSentences:
    """
    Download audio files from tatoeba using audio IDs listen in a JSONl
    
    Attributes:
        json_file (str): Path to the JSON file containg audio IDs.
        destination_directory (str): Directory where download audio files will be saved

    """
    
    def __init__(self, 
                jsonl_file:str,
                destination_directory:str):
        
        self.jsonl_file = jsonl_file
        self.destination_directory = destination_directory
        
    def _json_download(self):
        """
        Download MP3 audio files from tatoeba using IDs in the JSONL file

        For each audio ID, it sends GET request to tatoeba and save the audio file
        as an MP3 in the specified destination directory

        Logs success or error messages for each download attempt.
        """
        
        os.makedirs(self.destination_directory, exist_ok= True)

        with open(self.jsonl_file, "r" , encoding = "utf-8") as f:
            data = json.load(f)

        for item in data:
            audio_id = item["audio_id"]
            url = f"https://tatoeba.org/audio/download/{audio_id}"
            file_name = f"{audio_id}.mp3"
            complete_path = os.path.join(self.destination_directory, file_name)
        
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(complete_path, "wb") as f:
                        f.write(response.content)
                        print(f"AUDIO DOWNLOAD CORRECTLY {audio_id}")
                else:
                    print(f"ERROR WITH THE AUDIO {audio_id}")
            except Exception as e:
                print(f"ERROR WITH THE AUDIO {audio_id}")