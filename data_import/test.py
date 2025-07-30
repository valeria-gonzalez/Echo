from import_words import ImportWords
from import_texts import ImportTexts
from import_sentences import ImportSentences
from import_audio_sentences import ImportAudioSentences
from import_audio_texts import ImportAudioTexts

def main():

    #words
    api_direction_words = "http://127.0.0.1:8000/resources/words"
    jsonl_direction_words = "../data_processing/dataset_manager/processed_datasets/words_processed.jsonl"

    #sentences
    api_direction_sentences = "http://127.0.0.1:8000/resources/sentences"
    jsonl_direction_sentences = "../data_processing/dataset_manager/processed_datasets/sentences_processed.jsonl"

    #texts
    api_direction_texts = "http://127.0.0.1:8000/resources/texts"
    jsonl_direction_texts = "../data_processing/dataset_manager/processed_datasets/texts_processed.jsonl"

    #sentences Audio
    api_direction_sentences_audio = "http://127.0.0.1:8000/resources/sentences/audios"
    download_audio = './data_download/audios'

    #texts Audio
    direction_texts_audio = "./../data_processing/texts/datasets/chapters/group_1_audios"
    api_direction_texts_audio = "http://127.0.0.1:8000/resources/texts/audios"

    importWords = ImportWords(api_direction_words, jsonl_direction_words)
    importSentences = ImportSentences(api_direction_sentences, jsonl_direction_sentences)
    importTexts = ImportTexts(api_direction_texts,jsonl_direction_texts)
    importAudioSentences = ImportAudioSentences(api_direction_sentences_audio, download_audio)
    importAudioTexts = ImportAudioTexts(direction_texts_audio)

    #importWords._jsonl_import()
    #importSentences._json_import()
    importTexts._jsonl_import()

    #importAudioSentences._audio_import_sentences()  
    
    path_list = importAudioTexts._extract_chapter_directories()

    for path in path_list:
        importAudioTexts._import_audio_texts(directory_local=path, post_directory=api_direction_texts_audio)


if __name__ == "__main__":
    main()