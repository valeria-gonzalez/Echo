from word_processing import WikiExtractProcessor

def main():
    filepath = "datasets/raw-wiktextract-data.jsonl"
    processor = WikiExtractProcessor(word_dump_filepath=filepath)
    total_words = processor.get_words_JSONL(max_words=200, words_per_file=200)
    print(f"{total_words} words extracted.")
    
if __name__ == "__main__":
    main()