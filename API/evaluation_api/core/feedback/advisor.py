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
        prompt = f"""You are a supportive speech coach helping an English learner 
        improve their pronunciation and speaking style.

        Compare the user's delivery to the original audio based on the data 
        below, and give personal, plain-language feedback.

        Structure your response into these four categories (in this order):
        - **Speed**
        - **Clarity**
        - **Articulation**
        - **Rythm**

        In each:
        - Start with a positive bullet point (even if no improvements are needed).
        - Then two bullet points on how to improve.
        - Avoid technical terms like "articulation rate", "speech rate", "transcription", "speaking ratio".
        - Avoid refering to the categories in the feedback.
        - Refer to the reference strictly as "original audio".

        If no improvements are needed for a category, still include it with a bullet like:
        - "You're doing great with [category]. Keep it up!"

        **Do not skip any category. Respond only with bullet points. No introductions, summaries, or extra explanation.**
        ---

        **Original Audio**:
        - Syllables: {reference_audio_analysis["number_of_syllables"]}
        - Pauses: {reference_audio_analysis["number_of_pauses"]}
        - Speech rate: {reference_audio_analysis["speech_rate"]}
        - Articulation rate: {reference_audio_analysis["articulation_rate"]}
        - Speaking time (no pauses): {reference_audio_analysis["speaking_duration"]}
        - Total time: {reference_audio_analysis["total_duration"]}
        - Speaking ratio: {reference_audio_analysis["ratio"]}

        **User Audio**:
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
        
        try:
            response = requests.post(self.API_URL, headers=headers, data=payload)
            response_json = response.json()
            
            if (
            isinstance(response_json, dict)
            and "choices" in response_json
            and isinstance(response_json["choices"], list)
            and response_json["choices"]
            and "text" in response_json["choices"][0]
            ):
                return response_json["choices"][0]["text"]

            print("Warning: Unexpected API response structure")
            return ""
        
        except Exception as e:
            print(f"Error obtaining feedback: {e}")
            return ""
    
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
        It includes speed_tip, clarity_tip, articulation_tip, rythm_tip.

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
        MAX_RETRIES = 3
        for attempt in range(1, MAX_RETRIES + 1):
            response = self._make_api_request(prompt)
            if response.strip():
                break
            print(f"Retry attempt {attempt} failed. Retrying...")
        
        if not response.strip():
            return {
                "speed_tip": ["We're sorry, no feedback was generated."],
                "clarity_tip": ["Please try again later."],
                "articulation_tip": [],
                "rythm_tip": []
            }
            
        recommendations = self._parse_response(response)
        
        if not recommendations:
            return {
                "speed_tip": ["We're sorry, no useful feedback was found in the response."],
                "clarity_tip": ["Please try again later."],
                "articulation_tip": [],
                "rythm_tip": []
            }
            
        for key in ["speed_tip", "clarity_tip", "articulation_tip", "rythm_tip"]:
            if key not in recommendations:
                recommendations[key] = ["No feedback available."]
        
        return recommendations
        
        
        
    
        