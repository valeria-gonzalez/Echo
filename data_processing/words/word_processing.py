import json
import uuid
from collections import defaultdict
from typing import List

class WikiExtractProcessor:
    def __init__(self, word_dump_filepath:str):
        """Initialize WikiExtract Processor with filepath with word dump.

        Args:
            filepath (str): Name of the file 
        """
        self.accumulated_words = defaultdict(lambda: None)
        self.word_dump_filepath = word_dump_filepath
        self.total_words = 0
        self.words_per_file = 5000
    
    def extract_word_from_json(self, obj:dict)->dict:
        """Extract the relevant keys for a word from a JSON object. The keys
        are: `word`, `pos` (part of speech), `definitions`, `ipa`, `mp3_url`, 
        and `translation`.  

        Args:
            obj (dict): JSON object.

        Returns:
            dict: Dicitonary with word information.
        """
        # Check that the word is in english
        language = obj.get("lang")
        
        if language != "English":
            return None
        
        # Retrieve significant keys
        word = obj.get("word")
        part_of_speech = obj.get("pos")
        senses = obj.get("senses")
        sounds = obj.get("sounds")
        translations = obj.get("translations")
        
        # Needed variables
        unique_definitions = None
        ipa = None
        mp3_url = None
        spanish_translation = None
        
        # Definitions 
        # [{senses: {glosses: x}}]
        if senses:
            definitions = list() # Save all definitions for the word
            for item in senses:
                if item.get("glosses"):
                    definitions += item["glosses"]

            # Eliminate duplicate definitions
            unique_definitions = list(set(definitions))
                            
        # Audio file and IPA pronunciation 
        # [{sounds: {ipa: x, mp3_url: x}}]
        if sounds:
            for item in sounds:
                if ipa and mp3_url:
                    break
                
                if ipa == None and item.get("ipa"):
                    ipa = item["ipa"]
                    
                if mp3_url == None and item.get("mp3_url"):
                    mp3_url = item["mp3_url"]
        
        # Spanish translation
        # [{translation: {lang: x, word: x}}]
        if translations:
            for item in translations:
                if spanish_translation:
                    break
                
                if item.get("lang") and item.get("word"):
                    if(item["lang"] == "Spanish"):
                        spanish_translation = item["word"]
                        
        # Add information to dictionary
        word_obj = {
            "word": word,
            "pos" : part_of_speech,
            "definitions" : unique_definitions,
            "ipa": ipa,
            "mp3_url" : mp3_url,
            "translation" : spanish_translation,
        }
        
        return word_obj
    
    def remove_incomplete_words(self)->None:
        """ 
        Eliminate words that have empty keys from the accumulated words 
        dictionary.
        """
        incomplete_words = list()
        
        # Save words with incomplete fields
        for word, info in self.accumulated_words.items():
            if None in info.values():
                incomplete_words.append(word)
            
        # Eliminate words from dictionary  
        for word in incomplete_words:
            self.accumulated_words.pop(word)
            
    def save_words_to_JSONL(self, processed_dict:list)->None:
        """ 
        Write the accumulated words dictionary to a JSONL file. 
        """
        # Unique file name
        filename = f"datasets/words-{uuid.uuid4().hex}.jsonl"
        
        # Serializing json
        json_object = json.dumps(processed_dict)
        
        # Writing to sample.jsonl
        with open(filename, "w") as outfile:
            outfile.write(json_object + "\n")

    def accumulate_word(self, word_obj:dict)->None:
        """
        Add an extracted word to the accumulated words dictonary.

        Args:
            word_obj (dict): Dictionary with the word information.
        """
        # Extract keys
        word = word_obj["word"]
        part_of_speech = word_obj["pos"]
        definitions = word_obj["definitions"]
        ipa = word_obj["ipa"]
        mp3_url = word_obj["mp3_url"]
        translation = word_obj["translation"]

        # Insert a new word
        if word not in self.accumulated_words:
            self.accumulated_words[word] = {
                "definitions": [{
                    "pos": part_of_speech, 
                    "definitions": definitions
                    }] if part_of_speech and definitions else None,
                "ipa": ipa,
                "mp3_url": mp3_url,
                "translations": [translation] if translation else None,
            }
        # Update an existing word
        else:
            # Add translation
            if translation:
                if self.accumulated_words[word]["translations"] == None:
                    self.accumulated_words[word]["translations"] = list()
            
                self.accumulated_words[word]["translations"].append(translation)
            
            # Add definitions for a new part of speech
            if part_of_speech and definitions:
                if self.accumulated_words[word]["definitions"] == None:
                    self.accumulated_words[word]["definitions"] = list()
                
                # Check if there is a dictionary with pos in definitions list
                exists = False 
                for entry in self.accumulated_words[word]["definitions"]:
                    # Update pos definitions
                    if entry.get("pos") == part_of_speech:
                        entry["definitions"] += definitions
                        exists = True
                        break
                    
                # Create a new dictionary for the pos
                if not exists:
                    self.accumulated_words[word]["definitions"].append(
                                                    {"pos": part_of_speech,
                                                    "definitions": definitions})
                    
            # Update information on empty keys
            for key in ["ipa", "mp3_url"]:
                if not self.accumulated_words[word][key] and word_obj[key]:
                    self.accumulated_words[word][key] = word_obj[key]
                    
    def is_new_word(self, word:str)->bool:
        return word not in self.accumulated_words
    
    def reached_words_per_file(self)->bool:
        return len(self.accumulated_words) >= self.words_per_file
    
    def get_words_JSONL(self, max_words:int=-1, words_per_file:int=10000)->int:
        """Extracts up to `max_words` entries from the WikiExtract word dump.
        These words can be saved in multiple JSONL files with a specific
        amount of `words_per_file`.
        By default it will extract all words and save them in files with 10000 
        words each.

        Args:
            max_words (int, optional): Amount of words to extract. Defaults to -1.
            words_per_file (int, optional): Amount of words per JSONL file.
            Defaults to 10000.

        Returns:
            int: Total number of words successfully saved.
        """
        self.total_words = 0
        self.words_per_file = words_per_file
        
        with open(self.word_dump_filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                # Read max num of words
                if max_words != -1 and self.total_words >= max_words: break
                
                if line.strip(): 
                    try:
                        obj = json.loads(line) # Read line as json object
                        word_obj = self.extract_word_from_json(obj) 
                        
                        if word_obj != None: 
                            word = word_obj["word"]
                            
                            # Check that there's no new info for existing word
                            # and write accumulated words to JSONL
                            if self.is_new_word(word) and self.reached_words_per_file():
                                self.remove_incomplete_words() 
                                
                                if self.reached_words_per_file():
                                    processed_dict = self.prepare_words()
                                    self.save_words_to_JSONL(processed_dict)
                                    self.total_words += len(self.accumulated_words)
                                    self.accumulated_words.clear()
                            
                            self.accumulate_word(word_obj)
                        
                    except json.JSONDecodeError as e:
                        print(f"Error decoding line {i + 1}: {e}")
                        print(f"Line content: {line[:200]}")
                        continue
        
        # Check for remaining words          
        if(len(self.accumulated_words) > 0):
            self.remove_incomplete_words()
            
            if(len(self.accumulated_words) > 0):
                processed_dict = self.prepare_words()
                self.save_words_to_JSONL(processed_dict)
                self.total_words += len(self.accumulated_words)
                self.accumulated_words.clear()
            
        return self.total_words
    
    def prepare_words(self)->List[dict]:
        """Turn the accumulated words dictonary into a list of dictionaries where
        each dictionary has the information for a single word.

        Returns:
            List[dict]: A list of dictionaries.
        """
        processed_dict = list()
        
        for word, info in self.accumulated_words.items():
            word_dict = {
                "word" : word,
                "definitions": info["definitions"],
                "ipa": info["ipa"],
                "mp3_url": info["mp3_url"],
                "translations": info["translations"]
            }
            processed_dict.append(word_dict)
            
        return processed_dict
            