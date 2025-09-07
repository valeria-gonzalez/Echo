from llama_cpp import Llama
import json
import os

class LocalSpeechAdvisor:
    def __init__(self):
        self.model = None
        # Get the path to this script's directory
        base_path = os.path.dirname(os.path.abspath(__file__))
        #self.model_path = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
        self.model_path = "models/mistral-7b-instruct-v0.1.Q5_K_S.gguf"
        # Build absolute path to model in models/
        self.full_model_path = os.path.join(base_path, self.model_path)
        self.CONTEXT_SIZE = 4096
        self._load_model()
        self.invalid_responses = 0
        
    def _load_model(self)->None:
        """Load the local model into memory."""
        try:
            self.model = Llama(
                model_path=self.full_model_path, 
                n_ctx=self.CONTEXT_SIZE,
                verbose=False
            )
        except Exception as e:
            print(f"Error ocurred during local model load: {e}")
    
    def _reload_model(self):
        """Force reload of the model from disk."""
        self.model = None
        self._load_model()
            
    def _create_prompt(self, difference_analysis:dict, wer:float)->str: 
        """Generate a structured prompt for the speech coaching LLM.

        Args:
            difference_analysis (dict): Analysis of differences between user and reference analysis.
            wer (float): Word error rate between the user and reference transcription.

        Returns:
            str: Formatted prompt text for the LLM.
        """       
        prompt = f"""
        You are a speech coach helping an English learner improve their pronunciation.
        Your job is to compare the provided numerical analysis of the learners's speech compared to the also provided analysis of the original audio and return feedback.

        Return your answer ONLY in **valid JSON format**, exactly like this:

        {{"speed_tip": ["...", "...", "..." ],
        "clarity_tip": ["...", "...", "..."],
        "articulation_tip": ["...", "...", "..."],
        "rythm_tip": ["...", "...", "..."]}}

        Each list must:
        - Contain exactly three full sentences.
        - Be written in second person with a warm, friendly tone.
        - Each sentence must be a full and descriptive, do NOT be brief.
        - Each sentence should be different.
        - Start with one sentence ONLY describing how the user performed compared to the original audio.
        - Follow with one tip on what to improve and how to improve it.
        - End with one tip on how to improve in the future.

        Here are the differences between the user audio and the original audio:
        - Number of syllables: {difference_analysis["number_of_syllables"]}
        - Number of pauses: {difference_analysis["number_of_pauses"]}
        - Speech rate: {difference_analysis["speech_rate"]}
        - Articulation rate: {difference_analysis["articulation_rate"]}
        - Speaking time (no pauses): {difference_analysis["speaking_duration"]}
        - Total time (with pauses): {difference_analysis["total_duration"]}
        - Speaking ratio: {difference_analysis["ratio"]}
        - Word Error Rate (WER): {wer}

        Use this to guide your feedback:
        - Values close to 0 → very similar → give a positive comment and mild tips.
        - Values around ±0.3 → somewhat different → give encouraging suggestions.
        - Values above ±0.6 → very different → give direct improvement tips.
        - Positive values mean the user had more of that metric than the original audio.
        - Negative values mean the user had less of that metric.
        - WER (0-1): low = clear and intelligible, high = unclear and difficult to follow.
        - Address WER differences ONLY in *clarity_tip*.
        
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
            print(f"Error generating local model response: {e}")
            print(f"Response: {response}")
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
        print("Processing local api response...")
        open_dict = response.find('{')
        close_dict = response.find('}', open_dict)
        
        if open_dict == -1 or close_dict == -1:
            self.invalid_responses += 1
            print("Response was not in valid JSON format to begin with.")
            print(f"Response: {response}")
            return {}
        
        try:
            feedback_dict = json.loads(response[open_dict:close_dict+1])
        except json.JSONDecodeError:
            print(f"Error parsing response, was not in valid JSON format")
            print(f"Response: {response}")
            return {}
        
        print("Successfully parsed response!")
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
        
        MAX_TRIES = 3
        response_keys = ["speed_tip", "clarity_tip", "articulation_tip", "rythm_tip"]
        
        attempt = 1
        while attempt < MAX_TRIES:
            print(f"Making a request, attempt {attempt}...")
            response = self._generate_output(prompt)
            
            feedback_dict = self._parse_response(response)
            if (
                feedback_dict and 
                isinstance(feedback_dict, dict) and 
                all(key in response for key in response_keys)
            ):
                print("Successful response!")
                return feedback_dict
            print(f"Retry attempt {attempt} failed. Retrying...")
            
            if(self.invalid_responses == 2):
                print("The model doesn't seem to understand...")
                print("Reloading...This may take a second, do not interrupt...")
                self._reload_model()
                print("Will try again now...")
                attempt -= 1
            
            attempt += 1
        
        return {
            "speed_tip": ["We're sorry, no feedback was generated."],
            "clarity_tip": ["Please try again later."],
            "articulation_tip": [],
            "rythm_tip": []
        }