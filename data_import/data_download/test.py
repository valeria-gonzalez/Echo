from download_sentences import DownloadSentences

def main():

    jsonl_file = "../../data_processing/dataset_manager/processed_datasets/sentences_processed.jsonl"
    destination_directory = "audios"

    downloadSentences = DownloadSentences(jsonl_file,destination_directory)
    
    downloadSentences._json_download()

if __name__ == "__main__":
    main()