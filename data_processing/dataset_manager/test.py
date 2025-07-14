from dataset_manager import DatasetManager

def main():
    manager = DatasetManager(
        filepath_dataset_texts = "datasets/group_1_texts.jsonl",
        destination_path = "datasets/processed_datasets/",
        filepath_dataset_sentences = "datasets/tatoeba_sentences.jsonl",
        filepath_dataset_words = "datasets/words_dataset.jsonl"
    )
    
    manager.get_final_datasets()
        
    
if __name__ == "__main__":
    main()