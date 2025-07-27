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
    """Class to add difficulty, category, word_count and translation to resources."""
    def __init__(self, filepath_dataset_texts:str, filepath_dataset_sentences:str, 
                 filepath_dataset_words:str, destination_path:str):
        """Create an object to process datasets.

        Args:
            filepath_dataset_texts (str): JSONL with text information.
            filepath_dataset_sentences (str): JSONL with sentence information.
            filepath_dataset_words (str): JSONL with word information.
            destination_path (str): Directory where the datasets are.
        """
        self.difficulty_evaluator = TextDifficultyEvaluator()
        self.category_evaluator = TextCategoryEvaluator()
        self.translator = TextTranslator()
        self.filepath_dataset_texts = filepath_dataset_texts
        self.destination_path = destination_path
        self.filepath_dataset_sentences = filepath_dataset_sentences
        self.filepath_dataset_words = filepath_dataset_words
        
    def _process_texts(self) -> None:
        """Add difficulty, category, translation and word count to texts.

        Returns:
        (file): A new file called `texts_processed.jsonl`.
        """
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
        """Add difficulty, category and word count to sentences.

        Returns:
        (file): A new file called `sentences_processed.jsonl`.
        """
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
        """Add difficulty, category and syllable count to words.

        Returns:
        (file): A new file called `words_processed.jsonl`.
        """
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
        """Process texts, sentences and words by adding:
        - Difficulty (texts, sentences and words), 
        - Category (texts, sentences and words), 
        - Translation (texts),
        - Word count (texts, sentences),
        - Syllable count (words)
        Returns:
            (file) Three files: `words_processed.jsonl`, `sentences_processed.jsonl`,
            and `texts_processed.jsonl` in the specified directory.
        """
        self._process_texts()
        self._process_sentences()
        self._process_words()
        print("All datasets have been processed and saved successfully.")