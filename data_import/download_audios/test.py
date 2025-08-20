from download_sentences import DownloadSentences
from download_words import DownloadWords
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s -%(levelname)s - %(message)s'
)

def main():
    
    """
    test.py

    Main script for downloading audio files for sentences and words from Tatoeba.

    This script performs the following tasks:
    1. Configures logging for tracking the download process.
    2. Defines paths to the processed JSONL datasets for sentences and words.
    3. Defines local destination directories for downloaded audio files.
    4. Instantiates downloader objects:
        - DownloadSentences: Handles downloading of sentence audio files.
        - DownloadWords: Handles downloading of word audio files.
    5. Downloads all audio files by calling the `_json_download()` method on each downloader object.

    Logging:
        INFO: Provides updates on successful downloads and progress.
        ERROR: Reports any errors during audio downloads.

    Usage:
        Run this script directly to download all sentence and word audios:

            python test.py
    """

    sentences_jsonl_path = "../../data_processing/dataset_manager/processed_datasets/sentences_processed.jsonl"
    sentences_audio_dir = "audios_sentences"

    words_jsonl_path = "../../data_processing/dataset_manager/processed_datasets/words_processed.jsonl"
    words_audio_dir = "audios_words"

    sentences_downloader = DownloadSentences(jsonl_file= sentences_jsonl_path,
                                             destination_directory= sentences_audio_dir)


    words_downloader = DownloadWords(jsonl_file= words_jsonl_path,
                                     destination_directory= words_audio_dir)

    sentences_downloader._json_download()
    words_downloader._json_download()

if __name__ == "__main__":
    main()