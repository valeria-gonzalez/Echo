from llama_cpp import Llama
import json5
import os
import re

class LocalSpeechAdvisor:
    def __init__(self):
        self.model = None
        # Get the path to this script's directory
        base_path = os.path.dirname(os.path.abspath(__file__))
        #self.model_path = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
        self.model_path = "models/gemma-7b-it.Q5_K_M.gguf"
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
            print(f"Error ocurred during local model load: {e}")
            
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
        You will be given as input a numerical analysis of the differences between both deliveries.
        
        You must answer with a valid **JSON object**, with **EXACTLY** the following keys:
        - speed_tip
        - clarity_tip
        - articulation_tip
        - rythm_tip

        Each key is a list that must:
        - Have exactly three comma separated sentences, delimited by double quotes ("")
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
        
        Use this to guide your feedback:
        - Values close to 0 → very similar → give a positive comment and mild tips.
        - Values around ±0.3 → somewhat different → give encouraging suggestions.
        - Values above ±0.6 → very different → give direct improvement tips.
        - Positive values mean the user had more of that metric than the original audio.
        - Negative values mean the user had less of that metric.
        - WER (0-1): low = clear and intelligible, high = unclear and difficult to follow.
        
        Here is the numerical analysis of the differences between the user and the original audio you must give feedback on:

        - Syllables: {difference_analysis["number_of_syllables"]}
        - Pauses: {difference_analysis["number_of_pauses"]}
        - Speech rate: {difference_analysis["speech_rate"]}
        - Articulation rate: {difference_analysis["articulation_rate"]}
        - Speaking time (no pauses): {difference_analysis["speaking_duration"]}
        - Total time: {difference_analysis["total_duration"]}
        - Speaking ratio: {difference_analysis["ratio"]}
        - Transcription Error Rate (WER): {wer}

        
        Here's an example input:
        
        {{"number_of_syllables": 6, "number_of_pauses": 0, "speech_rate": 2.0, 
        "articulation_rate": 2.0, "speaking_duration": 5.6, 
        "total_duration": 6.0, "ratio": 0.9, 
        "transcription": "life is not an exact science it is an art"}}
        
        Here's the corresponding example output:
        {{
            "clarity_tip": [
                "There was some variation from the original audio; sometimes words weren't quite clear.",
                "Pay attention to making sure all parts of each word come through distinctly for better understanding.",
                "Practicing difficult sounds slowly can make them easier to say clearly over time."
            ],
            "speed_tip": [
                "Overall you were close to the pace of the original audio.",
                "Try slowing down just slightly when speaking so each word has enough space.",
                "Focusing on consistent pacing will help listeners understand every part of your message."
            ],
            "rythm_tip": [
                "Your rhythm felt very similar to the original audio.",
                "Think about emphasizing key words naturally while keeping everything flowing smoothly.",
                "A natural flow makes your communication feel effortless and engaging!"
            ],
            "articulation_tip": [
                "The way you formed certain sounds varied somewhat from the original audio.",
                "Imagine stretching out your mouth muscles before starting - this helps create more precise shapes!",
                "Being mindful about forming each sound fully will increase precision overall."
            ]
        }}
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
            print("Obtaining response from model...", end="")
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
            print("Success!")
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
        open_dict = response.rfind('{')
        close_dict = response.rfind('}')
        
        if open_dict == -1 or close_dict == -1:
            print("Response was not in valid JSON format to begin with.")
            print(f"Response: {response}")
            return {}
        
        json_str = response[open_dict:close_dict+1]

        # Normalize quotes
        json_str = json_str.replace("'", "\"").replace("”", "\"").replace("“", "\"")
        
        # Fix contractions like you"re -> you're
        json_str = re.sub(r'(\w)"(\w)', r"\1'\2", json_str)
        
        # Remove stray trailing commas (common model bug)
        json_str = re.sub(r",(\s*[}\]])", r"\1", json_str)

        print(f"Cleaned json string: {json_str}")
        
        try:
            feedback_dict = json5.loads(json_str)
            print("Successfully parsed response!")
            return feedback_dict
        except Exception as e:
            print(f"Error parsing response, could not form a valid JSON format")
            print(f"Error is: {e}")
            print(f"Response: {response}")
            return {}
    
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
            print(f"Making a request to local model, attempt {attempt}...")
            response = self._generate_output(prompt)
            feedback_dict = self._parse_response(response)
            
            if (
                    feedback_dict and 
                    isinstance(feedback_dict, dict) and 
                    all(key in response for key in response_keys)
                ):
                    print("Successful response!")
                    return feedback_dict
                
            print(f"Attempt {attempt} failed. Retrying...")    
            attempt += 1
            
        return {
            "speed_tip": ["We're sorry, no feedback was generated."],
            "clarity_tip": ["Please try again later."],
            "articulation_tip": [],
            "rythm_tip": []
        }