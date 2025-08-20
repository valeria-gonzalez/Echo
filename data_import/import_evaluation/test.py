from import_evaluation_sentences import ImportEvaluationSentences
from import_evaluation_words import ImportEvaluationWords
from import_evaluation_texts import ImportEvaluationTexts
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s -%(levelname)s - %(message)s'
)

def main():
    """
    test.py
    Main script for evaluating audio files of sentences, words, and texts.

    This script performs the following tasks:
    1. Configures logging for all operations.
    2. Sets the evaluation API endpoint.
    3. Defines API endpoints for updating evaluation results for words, sentences, and texts.
    4. Specifies local directories where audio files are stored.
    5. Initializes the corresponding evaluation classes:
        - ImportEvaluationSentences: Handles evaluation of sentence audios.
        - ImportEvaluationWords: Handles evaluation of word audios.
        - ImportEvaluationTexts: Handles evaluation of text audios.
    6. Retrieves evaluations for sentences and uploads results to the API.
    7. Retrieves evaluations for words and uploads results to the API.
    8. Extracts chapter directories and evaluates text audios, uploading results to the API.

    Logging:
        INFO: Provides updates on successful evaluations and progress.
        ERROR: Reports any errors during audio evaluations.

    Usage:
        Run this script directly to perform all audio evaluations and upload results:

            python3 test.py
    """

    #EVALUATION API
    evaluation_api = "http://127.0.0.1:8000/evaluation/analyze_audio"



    api_resources_update_evaluation_words = "http://127.0.0.1:8001/resources/words/evaluation"
    api_resources_update_evaluation_sentences = "http://127.0.0.1:8001/resources/sentences/evaluation"
    api_resources_update_evaluation_texts = "http://127.0.0.1:8001/resources/texts/evaluation"

    #local audios
    audio_direction_sentences = "../download_audios/audios_sentences"
    audio_direction_words = "../download_audios/audios_words"
    direction_texts_audio = "../../data_processing/texts/datasets/chapters/group_1_audios"
    


    import_evaluation_sentences = ImportEvaluationSentences(audio_download_path=audio_direction_sentences,
                                                          evaluation_api_url=evaluation_api,
                                                          evaluation_update_resources_url=api_resources_update_evaluation_sentences)

    import_evaluation_words = ImportEvaluationWords(audio_download_path=audio_direction_words,
                                                  evaluation_api_url=evaluation_api,
                                                  evaluation_update_resources_url=api_resources_update_evaluation_words)

    import_evaluation_texts = ImportEvaluationTexts(local_directory=direction_texts_audio,
                                                  evaluation_api_url=evaluation_api,
                                                  evaluation_update_resources_url=api_resources_update_evaluation_texts)

    import_evaluation_sentences._get_evaluation_sentences()

    
    import_evaluation_words._get_evaluation_words()


    path_list = import_evaluation_texts._extract_chapter_directories()

    for path in path_list:
        import_evaluation_texts._get_evaluation_texts(audio_download_path=path)


if __name__ == "__main__":
    main()