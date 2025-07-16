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
        
    def _create_prompt(self, difference_analysis:dict, wer:float)->str: 
        """Generate a structured prompt for the speech coaching LLM.

        Args:
            user_audio_analysis (dict): Analysis data from the user's audio.
            reference_audio_analysis (dict): Analysis data from the original audio.
            wer (float): Word error rate between the user and reference transcription.

        Returns:
            str: Formatted prompt text for the LLM.
        """       
        prompt = f"""You're a supportive speech coach helping an English learner improve their pronunciation.

        Your task is to provide **friendly, easy-to-understand feedback** comparing the user's delivery to the original audio.

        Organize the feedback into exactly four sections:
        - **Speed**
        - **Clarity**
        - **Articulation**
        - **Rythm**

        In each section:
        - Start with a positive bullet point (even if no improvement is needed).
        - Then give two tips for improvement, based on the data below.
        - Do not use technical terms like "speech rate", "transcription", etc.
        - Do not mention these categories in your feedback — only include the actual bullet points.
        - Refer to the reference as "original audio".

        Always give feedback for all four sections. Use bullet points only. 
        Do NOT include introductions, summaries, or extra explanation.
        ---
        Here are the **differences between the user and the original audio**:

        - Syllables: {difference_analysis["number_of_syllables"]}
        - Pauses: {difference_analysis["number_of_pauses"]}
        - Speech rate: {difference_analysis["speech_rate"]}
        - Articulation rate: {difference_analysis["articulation_rate"]}
        - Speaking time (no pauses): {difference_analysis["speaking_duration"]}
        - Total time: {difference_analysis["total_duration"]}
        - Speaking ratio: {difference_analysis["ratio"]}

        **Use this to guide your feedback**:
        - Small differences (less than ±0.1 for rates/times or ±1 for counts) = “very similar” → use a positive bullet.
        - Moderate differences (±0.1 - 0.5 or ±1 - 2) → suggest mild improvements.
        - Large differences (above ±0.5 or ±2) → suggest more direct improvement.
        - If a value is exactly 0 → say the user matched the original well.

        **Transcription Error Rate (WER)**: {wer}
        Use the transcription error rate only to judge *clarity*, and give gentle feedback if it's higher than 0.
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
            "temperature": 0.3,
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

    
    def get_feedback(self, difference_analysis:dict, wer:float)->dict:
        """Generate structured speech feedback comparing user and reference audio.
        It includes speed_tip, clarity_tip, articulation_tip, rythm_tip.

        Args:
            user_audio_analysis (dict): Analysis data from the user's audio.
            reference_audio_analysis (dict): Analysis data from the original audio.
            wer (float): Word error rate between the two transcriptions.

        Returns:
            dict: Feedback grouped under Speed, Clarity, Tone, and Phonetic Precision.
        """
        prompt = self._create_prompt(difference_analysis, wer)
        
        MAX_RETRIES = 3
        for attempt in range(1, MAX_RETRIES + 1):
            response = self._make_api_request(prompt)
            print(response)
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
        
        
        
    
        