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
        prompt = f"""You are a supportive speech coach helping an English learner improve their pronunciation.

        You must respond ONLY with friendly, easy-to-understand bullet-point feedback comparing the user's delivery to the original audio.

        Respond in EXACTLY four sections titled:
        - **Speed**
        - **Clarity**
        - **Articulation**
        - **Rythm**

        In each section:
        - Start with a positive bullet point (even if no improvement is needed).
        - Then give two clear, plain-language tips for improvement.
        - Do not use technical terms (like "speech rate", "transcription", etc).
        - Do not refer to the category names within the feedback.
        - Refer to the original speaker as "original audio" — never say "reference".

        **ONLY respond in bullet points.**
        ---

        Here are the differences between the user and the original audio:

        - Syllables: {difference_analysis["number_of_syllables"]}
        - Pauses: {difference_analysis["number_of_pauses"]}
        - Speech rate: {difference_analysis["speech_rate"]}
        - Articulation rate: {difference_analysis["articulation_rate"]}
        - Speaking time (no pauses): {difference_analysis["speaking_duration"]}
        - Total time: {difference_analysis["total_duration"]}
        - Speaking ratio: {difference_analysis["ratio"]}

        Transcription Error Rate (WER): {wer}

        Use this to guide your feedback:
        - Small differences (less than ±0.1 or ±1) = “very similar” → give a positive bullet and mild tips.
        - Moderate differences (±0.1 - 0.5 or ±1 - 2) → give gentle suggestions.
        - Large differences (above ±0.5 or ±2) → give stronger improvement tips.
        - If WER > 0 → mention it in Clarity only.
        
        """
        
        return prompt
    
    def _make_api_request(self, prompt: str) -> dict:
        """Send a prompt to the Arli AI API and retrieve the structured response."""

        # JSON schema to enforce format
        guided_schema = {
            "type": "object",
            "properties": {
                "speed_tip": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 3,
                    "maxItems": 3
                },
                "clarity_tip": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 3,
                    "maxItems": 3
                },
                "articulation_tip": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 3,
                    "maxItems": 3
                },
                "rythm_tip": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 3,
                    "maxItems": 3
                }
            },
            "required": ["speed_tip", "clarity_tip", "articulation_tip", "rythm_tip"]
        }

        # Payload for ArliAI
        payload = {
            "model": "Qwen3-14B",
            "prompt": prompt,
            "temperature": 0.3,
            "top_p": 0.9,
            "top_k": 40,
            "max_tokens": 1000,
            "min_tokens": 100,
            "repetition_penalty": 1.1,
            "guided_json": guided_schema
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.API_KEY}"
        }

        try:
            response = requests.post(self.API_URL, headers=headers, data=json.dumps(payload))
            print("RAW RESPONSE:", response.text)
            response_json = response.json()

            # Expect structured JSON response under choices[0].text
            if (
                isinstance(response_json, dict)
                and "choices" in response_json
                and isinstance(response_json["choices"], list)
                and response_json["choices"]
                and "text" in response_json["choices"][0]
            ):
                # The model is guided to return a valid JSON string
                return json.loads(response_json["choices"][0]["text"])

            print("Warning: Unexpected API response structure")
            return {}

        except Exception as e:
            print(f"Error obtaining feedback: {e}")
            return {}

    def get_feedback(self, difference_analysis: dict, wer: float) -> dict:
        """
        Generate structured speech feedback comparing user and reference audio.
        Returns speed_tip, clarity_tip, articulation_tip, rythm_tip.
        """
        MAX_RETRIES = 3
        response_keys = ["speed_tip", "clarity_tip", "articulation_tip", "rythm_tip"]
        
        prompt = self._create_prompt(difference_analysis, wer)
        for attempt in range(1, MAX_RETRIES + 1):
            response = self._make_api_request(prompt)
            print(response)
            if (
                isinstance(response, dict) and 
                all(key in response for key in response_keys)
            ):
                return response
            print(f"Retry attempt {attempt} failed. Retrying...")

        # Fallback if API fails or returns malformed output
        return {
            "speed_tip": ["We're sorry, no feedback was generated."],
            "clarity_tip": ["Please try again later."],
            "articulation_tip": [],
            "rythm_tip": []
        }
        