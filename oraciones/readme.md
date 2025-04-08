# Sentence pre processing

Extract and unite relevant information obtained from different files obtained from Tatoeba.org pertaining to english sentences, their spanish translation and audio files for the Echo english pronunciation evaluation app. 

## Description

In order to provide practice sentences for the project, information obtained from different files must be extracted to only save relevant fields. These fields will mainly be:
- English Sentence
- Spanish Sentence
- Audio Link

## Getting Started

###  Download files

All the original resources were obtained from [tatoeba.org](https://tatoeba.org/en/downloads). In order to execute this notebook, please download the following files and save them in a directory named `datasets`:

- **Section: Sentence pairs**

  - **File Description:** All sentences in language A that are translated into language B, along with the translations (download English - Spanish).
  - **Origin Filename:** `Sentence pairs in English-Spanish -YYYY-MM-DD.tsv`
  - **Filename Notebook:** `engspa_translations.tsv`
  - **Fields and structure:** Sentence id [tab] Text [tab] Translation_id [tab] Text

- **Section: Sentences (CC0)**

  - **File Description:** Contains all the sentences available under CC0 (Download two files, only sentences in Spanish and in English).
  - **Origin Filename:** `{eng/spa}_sentences_CC0.tsv`
  - **Filename Notebook:** Same
  - **Fields and structure:** Sentence id [tab] Lang [tab] Text [tab] Date last modified

- **Section: Sentences with audio**

  - **File Description:** Contains the ids of the sentences, in all languages, for which audio is available.
  - **Origin Filename:** `sentences_with_audio.csv`
  - **Filename Notebook:** Same
  - **Fields and structure:** Sentence id [tab] Audio id [tab] Username [tab] License [tab] Attribution URL

###  Generating Files

The `sentence_audios.ipynb` file must be executed before the `sentence_translations.ipynb` file. 

To save the final clean datasets, uncomment the final block of code in both notebooks. The resulting files will be:

- **Filename:** `english_audio_sen.csv`

  - **File Description:** Contains all the english sentences under the creative commons license that have an audio file. 
  - **Fields and structure:** id,audio_id,username,license,attribution_url

- **Filename:** `eng_spa_audio_sentences.csv`

  - **File Description:** Contains all the english sentences that have an audio file and a spanish translation. 
  - **Fields and structure:** eng_id,eng_sentence,spa_id,spa_sen,audio_id

All the ids that are referenced are those provided by the tatoeba database.

###  Note
Do not upload the files to the git repository.