# README – `test.py`

## Description

`test.py` is the main script designed to **import and upload audio files for sentences, texts, and words** to local API endpoints. 
This script automates the process of taking locally stored audio files and uploading them to the corresponding API endpoints for further use in applications such as language learning, text-to-speech systems, or NLP tasks.

The script uses three specialized import classes:

- **ImportAudioSentences**: Uploads sentence audio files to the API.
- **ImportAudioTexts**: Uploads text audio files organized by chapter.
- **ImportAudioWords**: Uploads word audio files to the API.

---

## Features

1. Configures **logging** to track progress and errors for all operations.
2. Sets API endpoints for sentence, text, and word audio uploads.
3. Defines local directories where audio files are stored.
4. Initializes import classes for sentences, texts, and words.
5. Uploads audio files for:
   - Sentences
   - Texts (organized by chapters)
   - Words

---

## Requirements

- Python 3.10+
- Required libraries:
  - `requests` (or the library used in your import classes)
  - `logging` (included in the standard library)
- Local API endpoints running on:
  - `http://127.0.0.1:8001/resources/sentences/audios`
  - `http://127.0.0.1:8001/resources/texts/audios`
  - `http://127.0.0.1:8001/resources/words/audios`
- Locally downloaded audio files for:
  - Sentences
  - Texts
  - Words

---

## Usage

1. Ensure your API endpoints are running locally.
2. Place your audio files in the specified directories:
   - `texts_audio_dir`
   - `sentences_audio_dir`
   - `words_audio_dir`
3. Run the script:

```bash
python3 test.py

project/
│
├─ data_processing/
│  └─ texts/
│     └─ datasets/
│        └─ chapters/
│           └─ group_1_audios/
│
├─ download_audios/
│  ├─ audios_sentences/
│  └─ audios_words/
│
├─ import_audio_sentences.py
├─ import_audio_texts.py
├─ import_audio_words.py
└─ test.py
