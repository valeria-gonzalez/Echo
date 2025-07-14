import requests

class TextTranslator:
    def __init__(self):
        self.FTAPI_URL = "https://ftapi.pythonanywhere.com/translate"   
        self.LIBRE_TRANSLATE_URL = "http://127.0.0.1:5000/translate" 
        
    def _make_request_ftapi(self, text:str) -> str:
        """Translate text with ftapi.

        Args:
            text (str): Text to translate.

        Returns:
            str: Translated text.
        """
        params = {
            "sl": "en",
            "dl": "es",
            "text": text  
        }
        
        response = requests.get(self.FTAPI_URL, params=params)
        json_response = response.json()
        translated_text = json_response["destination-text"]
        return translated_text
    
    def _make_request_libre_translate(self, text:str) -> str:
        """Translate text with libre translate.

        Args:
            text (str): Text to translate.

        Returns:
            str: Translated text.
        """
        payload = {
            "q": text,
            "source": "en",
            "target": "es",
            "api_key": ""  # Optional if self-hosted or not required
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(self.LIBRE_TRANSLATE_URL, json=payload, headers=headers)
        json_response = response.json()
        translated_text = json_response["translatedText"]
        return translated_text
    
    def translate_text(self, text:str, api:str="libre")->str:
        """Translate a text from english to spanish using either libretranslate
        (locally hosted) or ftapi (web).
        Args:
            text (str): Text in english to translate.
            api (str): Choose which api to use, either "ftapi" or "libre".

        Returns:
            str: Translated text.
        """
        if api == "libre":
            translated_text = self._make_request_libre_translate(text)
        else:
            translated_text = self._make_request_ftapi(text)
            
        return translated_text