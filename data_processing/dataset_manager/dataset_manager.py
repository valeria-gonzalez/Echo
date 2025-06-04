import os
import json
import sys

current_dir = os.path.dirname(os.path.abspath('__file__'))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from text_difficulty.text_difficulty import TextDifficultyEvaluator
from texts_by_category.text_category_evaluator import TextCategoryEvaluator

class DatasetManager:
    def __init__(self):
        self.difficulty_evaluator = TextDifficultyEvaluator()
        self.category_evaluator = TextCategoryEvaluator()
        self.filepath_dataset_texts = "datasets/group_1_texts.jsonl"
        self.destination_path = "datasets/processed_datasets/"
        self.filepath_dataset_sentences = "datasets/tatoeba_sentences.jsonl"
        self.filepath_dataset_words = "datasets/words-de02e1507605431abd5d829d7e868af5.jsonl"
        
    def _process_texts(self) -> None:
        texts = []
        with open(self.filepath_dataset_texts, "r",
            encoding="utf-8") as file:
            data = json.load(file)
            
            print("Working on processing texts...")
            
            for item in data:
                transcript = item.get("transcript", "")
                text = transcript.get("full_text", "")
                formatted_text = text.lower().capitalize()
                transcript["full_text"] = formatted_text
                item["difficulty"] = self.difficulty_evaluator.text_difficulty(text)
                categories = self.category_evaluator.classify_words(text)
                three_keys = list(categories.keys())[:3]
                item["categories"] = three_keys
                
                texts.append(item)
                
            os.makedirs(self.destination_path, exist_ok=True)
            json_object = json.dumps(texts)
            with open(os.path.join(self.destination_path, 
            "texts_processed.jsonl"), 
            "w", encoding="utf-8") as out_file:
                out_file.write(json_object + "\n")
                
    def _process_sentences(self) -> None:
        sentences = []
        with open(self.filepath_dataset_sentences, "r",
            encoding="utf-8") as file:
            data = json.load(file)
            
            print("Working on processing sentences...")
            
            for item in data:
                text = item.get("eng_sen", "")
                item["difficulty"] = self.difficulty_evaluator.sentence_difficulty(text)
                categories = self.category_evaluator.classify_words(text)
                three_keys = list(categories.keys())[:3]
                item["categories"] = three_keys
                
                sentences.append(item)
                
            os.makedirs(self.destination_path, exist_ok=True)
            json_object = json.dumps(sentences)
            with open(os.path.join(self.destination_path, 
            "sentences_processed.jsonl"), 
            "w", encoding="utf-8") as out_file:
                out_file.write(json_object + "\n")
                
    def _process_words(self) -> None:
        with open(self.filepath_dataset_words, "r",
            encoding="utf-8") as file:
            
            print("Working on processing words...")
            
            for line in file:
                word_entry = json.loads(line)
                for word, word_data in word_entry.items():
                    word_data["difficulty"] = self.difficulty_evaluator.word_difficulty(word)
                    all_texts = []
                    text = " "
                    definitions = word_data.get("definitions", [])
                    definition_texts = definitions[0].get("definitions", [])
                    all_texts.extend(definition_texts)
                    text = " ".join(all_texts)
                    categories = self.category_evaluator.classify_words(text)
                    three_keys = list(categories.keys())[:3]
                    word_data["categories"] = three_keys
                    
            os.makedirs(self.destination_path, exist_ok=True)
            json_object = json.dumps(word_entry)
            with open(os.path.join(self.destination_path, 
            "words_processed.jsonl"), 
            "w", encoding="utf-8") as out_file:
                out_file.write(json_object + "\n")
                
    def get_final_datasets(self) -> None:
        self._process_texts()
        self._process_sentences()
        self._process_words()
        print("All datasets have been processed and saved successfully.")