from sentence_processing import TatoebaProcessor

def main():
    processor = TatoebaProcessor(
        eng_sentences="datasets/eng_sentences_CC0.tsv",
        eng_spa_pairs="datasets/engspa_translations.tsv",
        sentences_with_audio="datasets/sentences_with_audio.csv"
    ) 
    
    processor.get_sentences_csv()
    processor.get_sentences_jsonl()

if __name__ == "__main__":
    main()