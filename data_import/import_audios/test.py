
from import_audio_sentences import ImportAudioSentences
from import_audio_texts import ImportAudioTexts
from import_audio_words import ImportAudioWords
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s -%(levelname)s - %(message)s'
)

def main():
    """
    test.py
    Main script for importing and uploading audio files for sentences, texts, and words.

    This script performs the following tasks:
    1. Configures logging for all operations.
    2. Sets API endpoints for sentences, texts, and words.
    3. Defines local directories where audio files are stored.
    4. Initializes the corresponding import classes:
        - ImportAudioSentences: Handles sentence audio uploads.
        - ImportAudioTexts: Handles text audio uploads.
        - ImportAudioWords: Handles word audio uploads.
    5. Uploads sentence audio files to the API.
    6. Extracts chapter directories and uploads text audio files to the API.
    7. Uploads word audio files to the API.

    Logging:
        INFO: Provides updates on successful uploads and progress.
        ERROR: Reports any errors during file uploads.

    Usage:
        Run this script directly to perform all audio imports and uploads:

            python3 test.py
    """
    #API ENDPOINTS
    sentences_api_url = "http://127.0.0.1:8001/resources/sentences/audios"
    texts_api_url = "http://127.0.0.1:8001/resources/texts/audios"
    words_api_url = "http://127.0.0.1:8001/resources/words/audios"
    

    #LOCAL DIRECTORIES
    texts_audio_dir = "../../data_processing/texts/datasets/chapters/group_1_audios"
    sentences_audio_dir = "../download_audios/audios_sentences"
    words_audio_dir = "../download_audios/audios_words"


    # Initialize import classes
    import_audio_sentences = ImportAudioSentences(api_url=sentences_api_url,
                                                  download_dir=sentences_audio_dir)
    
    import_audio_texts = ImportAudioTexts(corpus_directory=texts_audio_dir)

    import_audio_words = ImportAudioWords(upload_api_url=words_api_url,
                                          download_dir=words_audio_dir)

    

    # Upload sentence audios
    import_audio_sentences._audio_import_sentences()  
    
    # Upload text audios
    path_list = import_audio_texts._extract_chapter_directories()
    for path in path_list:
        import_audio_texts._import_audio_texts(directory_local=path,
                                               post_directory=texts_api_url)

    # Upload word audios
    import_audio_words._audio_import_words()


if __name__ == "__main__":
    main()