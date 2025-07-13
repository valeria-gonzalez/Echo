import requests
import json
import re
from collections import defaultdict

from config import ARLI_API_KEY
class SpeechAdvisor:
    """Class that takes two audio analysis and returns recommendations."""
    def __init__(self):
        self.API_KEY = None
        self._load_api_key()
        self.API_URL = "https://api.arliai.com/v1/completions"
        
    def _load_api_key(self):
        """Load the API key from the config file."""
        self.API_KEY = ARLI_API_KEY
        
    def _create_prompt(self, user_audio_analysis:dict, 
                       reference_audio_analysis:dict, wer:float)->str: 
        """Generate a structured prompt for the speech coaching LLM.

        Args:
            user_audio_analysis (dict): Analysis data from the user's audio.
            reference_audio_analysis (dict): Analysis data from the original audio.
            wer (float): Word error rate between the user and reference transcription.

        Returns:
            str: Formatted prompt text for the LLM.
        """       
        prompt = f"""You are a friendly and supportive speech coach helping an
        English learner improve their pronunciation and speaking style.

        Compare the user's delivery with the reference speaker using the data 
        provided. Based on the differences, give helpful, plain-language feedback 
        that feels personal and encouraging.
        
        Your response must be grouped under these four categories:
        - **Speed**
        - **Clarity**
        - **Articulation**
        - **Rythm**
        
        Under each category:
        - Start with a short bullet point on what the user is doing well (if anything).
        - Then list any improvements needed and how to improve, also as bullet points.
        - Use simple, friendly, first-person language.
        - Do NOT use the technical terms provided in the overview (like “syllables per second” or “articulation rate”, "transcription error rate".).
        - Refer to the reference audio strictly as "original audio", do NOT refer to it as "reference" or "original".

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
    
    def _make_api_request(self, prompt:str)-> None:
        """Send a prompt to the Arli AI API and retrieve the generated response.
        Args:
            prompt (str): Prompt text to send to the LLM.

        Returns:
            str: Raw generated text from the API response.
        """
        payload = json.dumps({
            "model": "Qwen3-14B",
            "prompt": prompt,
            # Most important parameters
            "repetition_penalty": 1.1,
            "temperature": 0.5,
            "top_p": 0.9,
            "top_k": 40,
            "max_tokens": 1000,
            "stream": False,
            "n": 1,
            "min_tokens": 100,
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.API_KEY}"
        }

        response = requests.post(self.API_URL, headers=headers, data=payload)
        response_json = response.json()
        generated_text = response_json["choices"][0]["text"]
        return generated_text
    
    def _parse_response(self, text: str) -> dict:
        """Parse the LLM response into a structured dictionary format.

        Args:
            text (str): Raw text output from the LLM.

        Returns:
            dict: Parsed feedback grouped by category (e.g., Speed, Clarity).
        """
        feedback = defaultdict(list)
        current_category = None

        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            # Detect category titles like "**Speed**"
            match = re.match(r"- \*\*(.+?)\*\*", line)
            if match:
                current_category = match.group(1).lower() + "_tip"
                feedback[current_category] = []
            elif line.startswith("-") and current_category:
                # Remove leading dash and space
                cleaned_line = line.lstrip("- ").strip()
                feedback[current_category].append(cleaned_line)

        return dict(feedback)

    
    def get_feedback(self, user_audio_analysis:dict, 
                       reference_audio_analysis:dict, wer:float)->dict:
        """Generate structured speech feedback comparing user and reference audio.

        Args:
            user_audio_analysis (dict): Analysis data from the user's audio.
            reference_audio_analysis (dict): Analysis data from the original audio.
            wer (float): Word error rate between the two transcriptions.

        Returns:
            dict: Feedback grouped under Speed, Clarity, Tone, and Phonetic Precision.
        """
        prompt = self._create_prompt(user_audio_analysis, 
                                     reference_audio_analysis, 
                                     wer)
        response = self._make_api_request(prompt)
        recommendations = self._parse_response(response)
        return recommendations
        
        
        
    
        