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
    audio_dest_directory = "datasets/audio_segments"
    processor.combine_chapter_group_audios(chapters_directory, 
                                           audio_dest_directory,
                                           audio_length=30,
                                           verbose=True)
    
if __name__ == "__main__":
    main()