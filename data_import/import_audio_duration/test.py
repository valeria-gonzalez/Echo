from import_audio_duration import ImportAudioDuration
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s -%(levelname)s - %(message)s'
)

def main():
    """
    test.py

    Main script for calculating and updating the duration of audio files for sentences, words, and texts.

    This script performs the following tasks:
    1. Configures logging for tracking the process.
    2. Sets API endpoints for updating audio durations for words, sentences, and texts.
    3. Defines local directories where audio files are stored.
    4. Initializes the ImportAudioDuration class with the directories and API endpoints.
    5. Processes all audio files and updates their durations in the corresponding API endpoints.

    Logging:
        INFO: Provides updates on successful duration extraction and uploads.
        ERROR: Reports any errors during audio processing.

    Usage:
        Run this script directly to calculate and upload audio durations:

            python3 test.py
    """


    api_resources_update_audio_duration_words = "http://127.0.0.1:8001/resources/words/audio_duration"
    api_resources_update_audio_duration_sentences = "http://127.0.0.1:8001/resources/sentences/audio_duration"
    api_resources_update_audio_duration_texts = "http://127.0.0.1:8001/resources/texts/audio_duration"


    texts_audio_dir = "../../data_processing/texts/datasets/chapters/group_1_audios"
    sentences_audio_dir = "../download_audios/audios_sentences"
    words_audio_dir = "../download_audios/audios_words"
    import_audio_duration = ImportAudioDuration(
                                                local_directory_sentences = sentences_audio_dir,
                                                local_directory_words = words_audio_dir,
                                                local_directory_texts = texts_audio_dir,
                                                api_resources_put_audio_duration_sentences = api_resources_update_audio_duration_sentences,
                                                api_resources_put_audio_duration_words = api_resources_update_audio_duration_words,
                                                api_resources_put_audio_duration_texts = api_resources_update_audio_duration_texts
                                                )

    import_audio_duration._sentences()
    import_audio_duration._words()
    import_audio_duration._texts()

if __name__ == "__main__":
    main()