from text_processing import LibriSpeechProcessor

def main():
    dest_directory = "datasets/chapters"
    
    processor = LibriSpeechProcessor(
        corpus_directory="datasets/LibriSpeech/dev-clean"
    )
    
    processor.create_chapters_directory(group_length=100, 
                                        dest_directory=dest_directory,
                                        verbose=False
                                        )
    
if __name__ == "__main__":
    main()