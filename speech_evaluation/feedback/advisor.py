import requests
import json
from config import ARLI_API_KEY
class SpeechAdvisor:
    """Class that takes two audio analysis and returns recommendations."""
    def __init__(self):
        self.API_KEY = None
        self._load_api_key()
        self.API_URL = "https://api.arliai.com/v1/completions"
        
    def _load_api_key(self):
        self.API_KEY = ARLI_API_KEY
        
    def _create_prompt(self, user_audio_analysis:dict, 
                       reference_audio_analysis:dict, wer:float)->str:
        
        prompt = f"""You are a friendly and supportive speech coach helping an
        English learner improve their pronunciation and speaking style. 

        Compare the user's delivery with the reference speaker using the data 
        provided. Based on the differences, give helpful, non-technical feedback
        that feels personal and encouraging.
        
        Focus on key aspects like:
        - Rhythm and pacing
        - Clarity and articulation
        - Confidence and flow
        
        Avoid using technical terms (e.g., “syllables per second” or 
        “articulation rate”). Instead, explain in simple language how the user
        sounds and how they can sound more like the reference.

        Please return your response in this format only:
        - What you're doing well
        - What to improve
        - How to improve

        Respond ONLY with the bullet points. 
        Do NOT explain what you are doing, do NOT include any introductory 
        phrases, and do NOT repeat or summarize the prompt.
        ---

        **Reference Speaker Overview**:
        - Syllables: {reference_audio_analysis["number_of_syllables"]}
        - Pauses: {reference_audio_analysis["number_of_pauses"]}
        - Speech rate: {reference_audio_analysis["speech_rate"]} 
        - Articulation rate: {reference_audio_analysis["articulation_rate"]}
        - Speaking time (no pauses): {reference_audio_analysis["speaking_duration"]}
        - Total time: {reference_audio_analysis["total_duration"]}
        - Speaking ratio: {reference_audio_analysis["ratio"]}

        **User Overview**:
        - Syllables: {user_audio_analysis["number_of_syllables"]}
        - Pauses: {user_audio_analysis["number_of_pauses"]}
        - Speech rate: {user_audio_analysis["speech_rate"]} 
        - Articulation rate: {user_audio_analysis["articulation_rate"]}
        - Speaking time (no pauses): {user_audio_analysis["speaking_duration"]}
        - Total time: {user_audio_analysis["total_duration"]}
        - Speaking ratio: {user_audio_analysis["ratio"]}

        **Transcription Error Rate (WER)**: {wer}
        """

        return prompt
    
    def _make_api_request(self, prompt:str)->None:
        payload = json.dumps({
            "model": "Qwen3-14B",
            
            "prompt": prompt,

            # Most important parameters
            "repetition_penalty": 1.1,
            "temperature": 0.5,
            "top_p": 0.9,
            "top_k": 40,
            "max_tokens": 256,
            "stream": False,
            "n": 1,
            "min_tokens": 20,
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.API_KEY}"
        }

        response = requests.post(self.API_URL, headers=headers, data=payload)
        response_json = response.json()
        generated_text = response_json["choices"][0]["text"]
        print(generated_text)
        
        
        
    
        