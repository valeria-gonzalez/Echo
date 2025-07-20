from llama_cpp import Llama
import json
import os

class LocalSpeechAdvisor:
    def __init__(self):
        self.model = None
        # Get the path to this script's directory
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.model_path = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
        # Build absolute path to model in models/
        self.full_model_path = os.path.join(base_path, self.model_path)
        self.CONTEXT_SIZE = 2048
        self._load_model()
        
    def _load_model(self)->None:
        """Load the local model into memory."""
        try:
            self.model = Llama(
                model_path=self.full_model_path, 
                n_ctx=self.CONTEXT_SIZE,
                verbose=False
            )
        except Exception as e:
            print(f"Error ocurred during model load: {e}")
            
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

        {{"speed_tip": ["...", "...", "..." ],
        "clarity_tip": ["...", "...", "..."],
        "articulation_tip": ["...", "...", "..."],
        "rythm_tip": ["...", "...", "..."]}}

        Each list must:
        - Have exactly three comma separated sentences.
        - Be written in second person and a warm, friendly tone.
        - Each item must be a full, descriptive sentence, do NOT be brief.
        - Each item should be different.
        - Start with one comment ONLY describing how the user performed compared to the original audio.
        - Follow with one tip on what to improve and how to improve it.
        - End with one tip on how to improve in the future.
        
        Also:
        - Avoid technical terms like "transcription", "speech rate", etc.
        - Never refer to category names in the tips.
        - Refer to the original speaker as "original audio" (not "reference").
        - Do not mention reading aloud, recording yoursel, listening to native speakers.
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
    
    def _generate_output(self, prompt:str)->str:
        """Use prompt to generate output from the model.

        Args:
            prompt (str): Prompt needed for the model.

        Returns:
            str: JSON structured string with model response.
        """
        try:
            response = self.model(
                prompt,
                max_tokens=800,
                temperature=0.2,
                repeat_penalty=1.2,
                presence_penalty=0.2,
                top_p=0.85,
                top_k=10,
                echo=False
            )
            generated_text = response["choices"][0]["text"]
            return generated_text
        except Exception as e:
            print(f"Error generating model response: {e}")
            return ""
        
    def _parse_response(self, response:str)->dict:
        """Parse the response obtained from the model and turn it into a valid
        dictionary. 

        Args:
            response (str): Response obtained from the model.

        Returns:
            dict: Returns a dictionary with keys speed_tip, clarity_tip, 
            articulation_tip, and rythm_tip.
        """
        open_dict = response.find('{')
        close_dict = response.rfind('}')
        
        if open_dict == -1 or close_dict == -1:
            return {}
        
        try:
            feedback_dict = json.loads(response[open_dict:close_dict+1])
        except json.JSONDecodeError:
            return {}
        
        return feedback_dict
        
    
    def get_feedback(self, difference_analysis:dict, wer:float)->dict:
        """Generate structured speech feedback comparing user and reference audio.

        Args:
            difference_analysis (dict): Analysis of differences between user and reference analysis.
            wer (float): Word error rate between the user and reference transcription.

        Returns:
            dict: Returns a dictionary with keys speed_tip, clarity_tip, 
            articulation_tip, and rythm_tip.
        """
        prompt = self._create_prompt(difference_analysis, wer)
        
        MAX_TRIES = 2
        response_keys = ["speed_tip", "clarity_tip", "articulation_tip", "rythm_tip"]
        
        for attempt in range(1, MAX_TRIES + 1):
            response = self._generate_output(prompt)
            print(f"Response: {response}")
            feedback_dict = self._parse_response(response)
            if (
                isinstance(feedback_dict, dict) and 
                all(key in response for key in response_keys)
            ):
                return feedback_dict
            print(f"Retry attempt {attempt} failed. Retrying...")
        
        return {
            "speed_tip": ["We're sorry, no feedback was generated."],
            "clarity_tip": ["Please try again later."],
            "articulation_tip": [],
            "rythm_tip": []
        }