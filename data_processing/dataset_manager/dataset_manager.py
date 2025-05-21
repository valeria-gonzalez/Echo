import os
import json
import sys

current_dir = os.path.dirname(os.path.abspath('__file__'))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from text_difficulty.text_difficulty import TextDifficultyEvaluator
from texts_by_category.text_category_evaluator import TextCategoryEvaluator

class DatasetManager:
    def __init__(self, texts_jsonl:str, dest_dir:str):
        self.difficulty_evaluator = TextDifficultyEvaluator()
        self.category_evaluator = TextCategoryEvaluator()
        self.filepath_dataset_texts = texts_jsonl
        self.destination_path = dest_dir
        
    def process_texts(self) -> None:
        with open(self.filepath_dataset_texts, "r", encoding="utf-8") as file:
            data = json.load(file)
            
            for item in data:
                key = item.get("chapter_id", "")
                transcript = item.get("transcript", "")
                text = transcript.get("full_text", "")
                formatted_text = text.lower().capitalize()
                transcript["full_text"] = formatted_text
                item["difficult"] = self.difficulty_evaluator.text_difficulty(text)
                print(f"Text difficulty for {key}: {item['difficult']}")
                
            os.makedirs(self.destination_path, exist_ok=True)
                
            with open(os.path.join(self.destination_path, "texts_processed.jsonl"),
                      "w", 
                      encoding="utf-8") as out_file:
                for item in data:
                    out_file.write(json.dumps(item, ensure_ascii=False) + "\n")