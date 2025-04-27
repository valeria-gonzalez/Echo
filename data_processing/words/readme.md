# Word preprocessing

## Objective

In order to provide practice words for the project, relevant information pertaining to english words must be extracted from the raw Wiktionary data dump provided by Wikiextract. 

Since the data file is very large, the objective of this step is not to unify all the entries in a single file, but to extract a specified amount of words and save a set amount of words per JSONL file. This is entirely up to the user's choosing. 

The needed information for a word is the following:

- English word
- Spanish word translation
- Word definitions
- IPA pronunciation
- Audio pronunciation file

## What is Wikiextract?

Wikiextract is a Python package and tool for extracting information from various Wiktionary data dumps, most notably and completely the English edition (enwiktionary). 

The English edition extraction 'module' extracts glosses, parts-of-speech, declension/conjugation information when available, translations for all languages when available, pronunciations (including audio file links), qualifiers including usage notes, word forms, links between words including hypernyms, hyponyms, holonyms, meronyms, related words, derived terms, compounds, alternative forms, etc.

Special thanks and acknowledgments to Wikiextract.

[Click here for more information.](https://github.com/tatuylonen/wiktextract)

## Dataset description

Wikiextract offers a pre-expanded data JSONL file for easier use, which is what is used for this project. The file can be obtained from the [Raw data downloads extracted from Wiktionary](https://kaikki.org/dictionary/rawdata.html).

The file to download is under the link: "Download raw Wiktextract data (JSONL, one object per line) (18.8GB) or compressed .gz (2.2GB)"

Please download the compressed version.

The resulting file is in a JSONL format, which has one JSON object per line. Given the large size of the file, this makes it much easier to process the data line-by-line.

**Disclaimer:** If you try to open the file in a preview mode, it most probably will not work.

### Format of the extracted word entries

The information returned for each word is a dictionary. The keys used in the dictionary has the following keys:

- `word`: (string) The word form.

- `pos` : (string) Part of speech, such as "noun", "verb", "adj", "adv", "pron", "determiner", "prep" (preposition), "postp" (postposition), and many others.

- `lang` : (string) Name of the language this word belongs to (e.g., English).

- `senses` : (list of dictionaries) List of word senses for this word/part-of-speech. Each word entry may have multiple glosses under the senses key. Each sense is a dictionary, the keys used were: 

  - `glosses`: (list of strings) List of glosses for the word.

- `sounds` : (list of dictionaries) Contains pronunciation, hyphenation, rhyming, and related information in multiple dictionaries. The keys used were:

  - `ipa` : (string) pronunciation specifications as an IPA string /.../ or [...]

  - `mp3_url` : (string) URL for an MP3 format sound file

- `translations`: (list of dictionaries) Non-disambiguated translation entries. The translations are stored in a list of dictionaries, the keys used were:

  - `lang` : the language name that the translation is for.

  - `word` : the translation in the specified language (may be missing when `note` is present)


## Getting Started

### 1. Install needed libraries

For this section, the following modules were used:
- json
- uuid
- collections

These modules can be installed individually or via the `requirements.txt` file located in the root directory. As a disclaimer, it will also install all the required modules needed for preprocessing words, sentences and texts.

To install using the `requirements.txt`use:

```
pip install -r requirements.txt
```

###  2. Download required files

In order to execute this module, please download the necessary file described above.

Needed file:

 - `raw-wiktextract-data.jsonl`

###  3. Usage

```
from word_processing import WikiExtractProcessor

def main():
    filepath = "datasets/raw-wiktextract-data.jsonl"
    processor = WikiExtractProcessor(word_dump_filepath=filepath)
    total_words = processor.get_words_JSONL(max_words=5000, words_per_file=5000)
    print(f"{total_words} words extracted.")
    
if __name__ == "__main__":
    main()
```

- `get_words_JSONL` : This method extracts up to `max_words` entries from the 
WikiExtract data dump JSONL file. These words can be saved in multiple JSONL 
files with a specific amount of `words_per_file`. By default it will extract all
words and save them in files with 10000 words each.

For example, if the parameters are `max_words=10000` and `words_per_file=2000`, 
five JSON files with 2000 words per file will be generated. 

This is done so that the user can decide how large they want the resulting 
files to be given that the WikiExtract Dump has more than 100,000 words.

#### Results

The resulting files after execution will be named `words-{unique_identifier}.json`. It will contain the amount of specified english words with their definitions depending on the part of speech, a list of spanish translations and an audio file link.

The file has the following keys:

- `word` : (string) The english word

- `definitions` : (list of dictionaries) A list of dictionaries with the definitions of a word according to its part of speech. It has the following keys:

  - `pos`: (string) Part of speech, such as "noun", "verb", "adj", "adv", "pron", "determiner", "prep" (preposition), "postp" (postposition), and many others.

  - `definitions`: (list of strings) List of definitions.

- `ipa` : (string) pronunciation specifications as an IPA string 

- `mp3_url` : (string) URL for an MP3 format sound file

- `translations` : (list of strings) Spanish translations of the word