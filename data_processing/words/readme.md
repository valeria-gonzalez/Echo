# Word preprocessing

## Objective

In order to provide practice words for the project, relevant information pertaining to english words must be extracted from the raw Wiktionary data dump provided by Wikiextract. 

Since the data file is very large, the objective of this step is not to unify all the entries in a single file, but to extract a specified amount of words and save a set amount of words per JSON file. This is entirely up to the user's choosing. 

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
- ipykernel
- ipython
- json
- uuid
- collections

These modules can be installed individually or via the `requirements.txt` file located in the root directory. As a disclaimer, it will also install all the required modules needed for preprocessing words, sentences and texts.

To install using the `requirements.txt`use:

```
pip install -r requirements.txt
```

###  2. Download required files

 In order to execute this notebook, please download the necessary file described above and save it in a directory named `datasets`.

 Needed file:

 - `raw-wiktextract-data.jsonl`

###  3. Execute `word_processing.ipynb`

Before executing the cells, feel free to change the parameters for the `process_words_from_file` function. 

This function extracts up to `max_words` entries from a JSONL file, saving them in batches of `batch_size` entries per output JSON file.

For example, if the parameters are `max_words=10000` and `batch_size=2000`, five JSON files with 2000 words per file will be generated. 

This is done so that the user can decide how large they want the resulting files to be. 

**Disclaimer:** If no parameters are given, the function will read the whole JSONL file and save the words in batches of 5000 words.

After specifying these parameters, please execute all the `word_preprocessing` notebook cells in order. This can be done by clicking the `Run All` option.

#### Final file description

The resulting files after execution will be named `words-{unique_identifier}.json`. It will contain the amount of specified english words with their definitions depending on the part of speech, a list of spanish translations and an audio file link.

The file has the following keys:

- `word` : (string) The english word

- `definitions` : (list of dictionaries) A list of dictionaries with the definitions of a word according to its part of speech. It has the following keys:

  - `pos`: (string) Part of speech, such as "noun", "verb", "adj", "adv", "pron", "determiner", "prep" (preposition), "postp" (postposition), and many others.

  - `definitions`: (list of strings) List of definitions.

- `ipa` : (string) pronunciation specifications as an IPA string 

- `mp3_url` : (string) URL for an MP3 format sound file

- `translations` : (list of strings) Spanish translations of the word