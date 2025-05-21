from dataset_manager import DatasetManager

def main():
    manager = DatasetManager(
        texts_jsonl="datasets/group_1_texts.jsonl",
        dest_dir="datasets/processed_datasets/"
    )
    manager.process_texts()
    
    
if __name__ == "__main__":
    main()