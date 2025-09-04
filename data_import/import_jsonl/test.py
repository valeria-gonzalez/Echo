from import_words import ImportWords
from import_texts import ImportTexts
from import_sentences import ImportSentences
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s -%(levelname)s - %(message)s'
)

def main():

    """
    test.py

    Main script for importing words, sentences, and texts from JSONL files to API endpoints.

    This script performs the following tasks:
    1. Configures logging to track the import process.
    2. Defines API endpoints for words, sentences, and texts.
    3. Specifies paths to the processed JSONL files for words, sentences, and texts.
    4. Initializes import classes:
        - ImportWords: Handles importing word entries to the words API.
        - ImportSentences: Handles importing sentence entries to the sentences API.
        - ImportTexts: Handles importing text entries to the texts API.
    5. Executes the import process for all data types, uploading entries to their respective API endpoints.

    Logging:
        INFO: Provides updates on successful imports and progress.
        ERROR: Reports any errors during the import process.

    Usage:
        Run this script directly to import all words, sentences, and texts:

            python test.py
    """

    
    words_api_url = "http://127.0.0.1:8001/resources/words"
    sentences_api_url = "http://127.0.0.1:8001/resources/sentences"
    texts_api_url = "http://127.0.0.1:8001/resources/texts"

    sentences_jsonl_path = "../../data_processing/dataset_manager/processed_datasets/sentences_processed.jsonl"
    words_jsonl_path = "../../data_processing/dataset_manager/processed_datasets/words_processed.jsonl"
    texts_jsonl_path = "../../data_processing/dataset_manager/processed_datasets/texts_processed.jsonl"



    import_words = ImportWords(words_api_url=words_api_url,
                               words_jsonl_path=words_jsonl_path)
    
    import_sentences = ImportSentences(sentences_api_url=sentences_api_url,
                                       sentences_jsonl_path=sentences_jsonl_path)
    
    import_texts = ImportTexts(texts_api_url=texts_api_url,
                               texts_jsonl_path=texts_jsonl_path)

    import_words._jsonl_import()
    import_sentences._json_import()
    import_texts._jsonl_import()
    
if __name__ == "__main__":
    main()