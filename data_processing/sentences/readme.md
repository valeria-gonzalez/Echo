# Sentence preprocessing

## Objective

In order to provide practice sentences for the project, relevant information pertaining to english sentences provided by different files from Tatoeba.org must be extracted and saved into a single file.

The needed information for a sentence is the following:

- English sentence
- Spanish sentence translation
- Link to audio pronunciation

## What is Tatoeba?

Tatoeba is a large database of sentences and translations. Its content is ever-growing and results from the voluntary contributions of thousands of members.

Tatoeba provides a tool for you to see examples of how words are used in the context of a sentence. You specify words that interest you, and it returns sentences containing these words with their translations in the desired languages.

Special thanks and acknowledgments to Tatoeba.

[Click here for more information](https://tatoeba.org/en/about).

## Dataset description

All the files used in this project were obtained from [tatoeba.org/downloads](https://tatoeba.org/en/downloads).

Tateoba offers data related to sentences under the creative commons license that is useful for developing language tools or processing data. Under a variety of categories, it's possible to download csv or tsv files containing information.

For the information needed for this project, the following files were used:

- **Category: Sentence pairs**

  - **File Description:** All sentences in language A that are translated into language B, along with the translations (download English - Spanish).
  - **Origin Filename:** `Sentence pairs in English-Spanish -YYYY-MM-DD.tsv`
  - **Fields and structure:** Sentence id [tab] Text [tab] Translation_id [tab] Text
  - **Note:** When downloading, please rename as `Sentence pairs in English-Spanish.tsv`

- **Category: Sentences (CC0)**

  - **File Description:** Contains all the sentences available under Creative Commons Zero (CC0) license in a specific language.
  - **Origin Filename:** `{eng/spa}_sentences_CC0.tsv`
  - **Fields and structure:** Sentence id [tab] Lang [tab] Text [tab] Date last modified
  - **Note:** Two files from this category are generated under the option "only sentences in Spanish" and "only sentences in English".

- **Section: Sentences with audio**

  - **File Description:** Contains the ids of the sentences, in all languages, for which audio is available.
  - **Origin Filename:** `sentences_with_audio.csv`
  - **Fields and structure:** Sentence id [tab] Audio id [tab] Username [tab] License [tab] Attribution URL
  - **Note:** A single sentence can have one or more audio, each from a different voice. To download a particular audio, use its audio id to compute the download URL. For example, to download the audio with the id 1234, the URL is https://tatoeba.org/audio/download/1234.

## Getting Started

### 1. Install needed libraries

For this section, the following modules were used:
- pandas 
- ipykernel
- ipython

These modules can be installed individually or via the `requirements.txt` file located in the root directory. As a disclaimer, it will also install all the required modules needed for preprocessing words, sentences and texts.

To install using the `requirements.txt`use:

```
pip install -r requirements.txt
```

###  2. Download required files

 In order to execute this notebook, please download the necessary files described above and save them in a directory named `datasets`.

 Needed files:

 - `Sentence pairs in English-Spanish.tsv`
 - `eng_sentences_CC0.tsv`
 - `spa_sentences_CC0.tsv`
 - `sentences_with_audio.csv`

###  3. Execute `sentence_preprocessing.ipynb`

Please execute the `sentence_preprocessing` notebook cells in order. This can be done by clicking the `Run All` option.

#### Final file description

The resulting file after execution will be named `eng_spa_audio_sentences.csv`. It will contain all the english sentences under the Creative Commons Zero (CCO) license that also have audio and a spanish translation.

The csv file is separated by commas as a delimiter. The file has the following fields:

- `eng_id` : Id of the english sentence in Tatoeba
- `eng_sentence` : Text of english sentence
- `spa_id` : Id of the spanish translation of the sentence in Tatoeba
- `spa_sentence` : Text of spanish translation sentence
- `audio_id` : Id of the audio pronunciation file of the english sentence

Below is the file description:

- **Filename:** `eng_spa_audio_sentences.csv`

  - **File Description:** Contains all the english sentences that have an audio file and a spanish translation. 
  - **Fields and structure:** eng_id,eng_sentence,spa_id,spa_sen,audio_id
