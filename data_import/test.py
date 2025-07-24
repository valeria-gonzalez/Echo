from import_words import ImportWords
from import_texts import ImportTexts
from import_sentences import ImportSentences

from import_audio_sentences import ImportAudioSentences

def main():

    #words
    api_direction_words = "http://127.0.0.1:8000/resourses/words"
    jsonl_direction_words = "../data_processing/dataset_manager/processed_datasets/words_processed.jsonl"

    #sentences
    api_direction_sentences = "http://127.0.0.1:8000/resourses/sentences"
    jsonl_direction_sentences = "../data_processing/dataset_manager/processed_datasets/sentences_processed.jsonl"

    #sentences audio
    api_direction_sentences_audio = "http://127.0.0.1:8000/resourses/sentences/audios"
    download_audio = './data_download/audios'
    
    #texts
    api_direction_texts = "http://127.0.0.1:8000/resourses/texts"
    jsonl_direction_texts = "../data_processing/dataset_manager/processed_datasets/texts_processed.jsonl"


    importWords = ImportWords(api_direction_words, jsonl_direction_words)
    importSentences = ImportSentences(api_direction_sentences, jsonl_direction_sentences)
    importTexts = ImportTexts(api_direction_texts,jsonl_direction_texts)

    importAudioSentences = ImportAudioSentences(api_direction_sentences_audio, download_audio)
    

    importWords.jsonlImport()
    importSentences.jsonImport()
    importTexts.jsonlImport()
    importAudioSentences.AudioImport()  


if __name__ == "__main__":
    main()