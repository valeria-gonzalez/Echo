import os
import json
import sys

current_dir = os.path.dirname(os.path.abspath('__file__'))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from text_difficulty.text_difficulty import TextDifficultyEvaluator
from texts_by_category.text_category_evaluator import TextCategoryEvaluator
from text_translate.text_translate import TextTranslator

class DatasetManager:
    def __init__(self, filepath_dataset_texts:str, filepath_dataset_sentences:str, 
                 filepath_dataset_words:str, destination_path:str):
        self.difficulty_evaluator = TextDifficultyEvaluator()
        self.category_evaluator = TextCategoryEvaluator()
        self.translator = TextTranslator()
        self.filepath_dataset_texts = filepath_dataset_texts
        self.destination_path = destination_path
        self.filepath_dataset_sentences = filepath_dataset_sentences
        self.filepath_dataset_words = filepath_dataset_words
        
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
                item["word_count"] = self.difficulty_evaluator._count_words(formatted_text)
                item["categories"] = three_keys
                item["translation"] = self.translator.translate_text(formatted_text)
                
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
                item["word_count"] = self.difficulty_evaluator._count_words(text)
                
                sentences.append(item)
                
            os.makedirs(self.destination_path, exist_ok=True)
            json_object = json.dumps(sentences)
            with open(os.path.join(self.destination_path, 
            "sentences_processed.jsonl"), 
            "w", encoding="utf-8") as out_file:
                out_file.write(json_object + "\n")
                
    def _process_words(self) -> None:
        words = []
        with open(self.filepath_dataset_words, "r",
            encoding="utf-8") as file:
            
            data = json.load(file)
            print("Working on processing words...")
            
            for item in data:
                text = item.get("word", "")
                item["difficulty"] = self.difficulty_evaluator.word_difficulty(text)
                categories = self.category_evaluator.classify_words(text)
                three_keys = list(categories.keys())[:3]
                item["categories"] = three_keys
                item["syllable_count"] = self.difficulty_evaluator._count_syllables(text)
                
                words.append(item)
                
            os.makedirs(self.destination_path, exist_ok=True)
            json_object = json.dumps(words)
            with open(os.path.join(self.destination_path, 
            "words_processed.jsonl"), 
            "w", encoding="utf-8") as out_file:
                out_file.write(json_object + "\n")
                
    def get_final_datasets(self) -> None:
        self._process_texts()
        self._process_sentences()
        self._process_words()
        print("All datasets have been processed and saved successfully.")