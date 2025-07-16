import json
import os
import requests
import datetime

class DownloadSentences:
    
    def __init__(self, 
                jsonl_file:str,
                destination_directory:str):
        self.jsonl_file = jsonl_file
        self.destination_directory = destination_directory
        
    def jsonDownload(self):
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