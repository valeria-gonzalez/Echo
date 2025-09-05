import requests
from json.decoder import JSONDecodeError
import json
from collections import defaultdict
from config import ARLI_API_KEY

class SpeechAdvisor:
    """Class that takes two audio analysis and returns recommendations."""
    def __init__(self):
        self.API_KEY = None
        self._load_api_key()
        # self.model = "Gemma-3-27B-it"
        self.API_URL = "https://api.arliai.com/v1/completions"
        
    def _load_api_key(self):
        """Load the API key from the config file."""
        self.API_KEY = ARLI_API_KEY
        
    def _create_prompt(self, difference_analysis:dict, wer:float)->str: 
        """Generate a structured prompt for the speech coaching LLM.

        Args:
            difference_analysis (dict): Analysis of differences between user and reference analysis.
            wer (float): Word error rate between the user and reference transcription.

        Returns:
            str: Formatted prompt text for the LLM.
        """       
        prompt = f"""You are a speech coach helping an English learner improve their pronunciation.

        Your job is to compare the user's delivery to the original audio and return feedback.

        Return your answer in **valid JSON format**, exactly like this:

        "speed_tip": ["...", "...", "..." ],
        "clarity_tip": ["...", "...", "..."],
        "articulation_tip": ["...", "...", "..."],
        "rythm_tip": ["...", "...", "..."]

        Each list must:
        - Be written in second person and a warm, friendly tone.
        - Do not be too long. Each item should be a single descriptive sentence.
        - Each item should be different.
        - Start with one comment ONLY describing how the user performed compared to the original audio.
        - Follow with one tip on what to improve and how to improve it.
        - End with one tip on how to improve in the future.
        - Avoid technical terms like "transcription", "speech rate", etc.
        - Never refer to category names in the tips.
        - Refer to the original speaker as "original audio" (not "reference").
        - Do not mention reading aloud, recording or listening to native speakers.
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
        - Small differences (less than ±0.1 or ±1) = “very similar” → give a positive comment and mild tips.
        - Moderate differences (±0.1 to 0.5 or ±1 to 2) = "close" → give gentle suggestions.
        - Large differences (above ±0.5 or ±2) = "varied" → give direct improvement tips.
        - If WER > 0 → address that in *clarity_tip* only.
        """
        
        return prompt
    
    def _make_api_request(self, prompt: str) -> dict:
        """Send a prompt to the Arli AI API and retrieve the structured response.

        Args:
            prompt (str): Prompt for the LLM model.

        Returns:
            dict: Dictionary with speed_tip, clarity_tip, articulation_tip, rythm_tip.
        """

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
            #"model": self.model,
            "prompt": prompt,
            "temperature": 0.2, # Lower temperature = faster + more deterministic
            "top_p": 0.7, #  Cumulative probability of the top tokens to consider
            "top_k": 5, # Number of top tokens to consider
            "max_tokens": 300, # Maximum number of tokens to generate per output sequence
            #"min_tokens": 50, # Minimum number of tokens to generate per output sequence
            "n" : 1, # Number of output sequences to return
            "repetition_penalty": 1.2, # Penalizes new tokens based on their frequency in the generated text so far
            "no_repeat_ngram_size": 4,  # Avoid repetitive phrasing (helps speed indirectly)
            "guided_json": guided_schema,
            "stop":["}"]
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.API_KEY}"
        }

        try:
            response = requests.post(self.API_URL, headers=headers, data=json.dumps(payload))
            response_json = response.json()

            # Expect structured JSON response under choices[0].text
            if (
                isinstance(response_json, dict)
                and "choices" in response_json
                and isinstance(response_json["choices"], list)
                and response_json["choices"]
                and "text" in response_json["choices"][0]
            ):
                try:
                    response_text = response_json["choices"][0]["text"]
                    return json.loads(response_text)
                except JSONDecodeError as e:
                    # Try to fix common problems: truncate at last full }
                    fixed = response_text.rsplit("}", 1)[0] + "}"
                    try:
                        return json.loads(fixed)
                    except JSONDecodeError as inner_e:
                        print(f"JSON decode failed after fix: {inner_e}")
                        return {}

            print("Warning: Unexpected ARLI API response structure")
            print(f"Response: {response_json}")
            return {}

        except Exception as e:
            print(f"Error obtaining ARLI API feedback: {e}")
            return {}

    def get_feedback(self, difference_analysis: dict, wer: float) -> dict:
        """Generate structured speech feedback comparing user and reference audio.

        Args:
            difference_analysis (dict): Analysis of differences between user and reference analysis.
            wer (float): Word error rate between the user and reference transcription.

        Returns:
            dict: Returns speed_tip, clarity_tip, articulation_tip, and rythm_tip.
        """
        prompt = self._create_prompt(difference_analysis, wer)
        
        MAX_RETRIES = 2
        response_keys = ["speed_tip", "clarity_tip", "articulation_tip", "rythm_tip"]
        
        for attempt in range(1, MAX_RETRIES + 1):
            response = self._make_api_request(prompt)
            if (
                isinstance(response, dict) and 
                all(key in response for key in response_keys)
            ):
                return response
            print(f"Retry attempt {attempt} failed. Retrying request...")

        # Fallback if API fails or returns malformed output
        return {
            "speed_tip": ["We're sorry, no feedback was generated."],
            "clarity_tip": ["Please try again later."],
            "articulation_tip": [],
            "rythm_tip": []
        }
        