from text_processing import LibriSpeechProcessor

def main():
    
    processor = LibriSpeechProcessor(
        corpus_directory="datasets/LibriSpeech/dev-clean",
        books_txt_filepath="datasets/LibriSpeech/BOOKS.TXT",
        chapters_txt_filepath="datasets/LibriSpeech/CHAPTERS.TXT"
    )
    
    # Extract chapters in groups
    chapters_dest_directory = "datasets/chapters"
    processor.create_chapters_directory(amount_of_chapters=100, 
                                        dest_directory=chapters_dest_directory,
                                        verbose=True)
    
    # Create 30s audios for each chapter
    chapters_directory = "datasets/chapters/group_1"
    audio_dest_directory = "datasets/chapters/group_1_audios"
    processor.combine_chapter_group_audios(chapters_directory, 
                                           audio_dest_directory,
                                           audio_length=30,
                                           verbose=True)
    
    # Create JSONL file for specified chapter directory
    json_filepath = "datasets/chapters/group_1_audios/texts.json"
    jsonl_filepath = "datasets/chapters/group_1_texts.jsonl"
    processor.get_texts_jsonl(json_filepath, jsonl_filepath, verbose=True)
    
if __name__ == "__main__":
    main()