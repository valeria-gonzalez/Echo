# README – `test.py`

## Description

`test.py` is the main script designed to **download audio files for sentences and words from Tatoeba**. This script automates the retrieval of audio files associated with processed datasets, saving them locally for further use in applications such as language learning, speech processing, or NLP tasks.

The script uses two specialized downloader classes:

- **DownloadSentences**: Downloads sentence audio files from the dataset.
- **DownloadWords**: Downloads word audio files from the dataset.

---

## Features

1. Configures **logging** to track download progress and errors.
2. Defines paths to the processed JSONL datasets for sentences and words.
3. Specifies local destination directories for downloaded audio files.
4. Instantiates downloader objects for sentences and words.
5. Executes the download process for all audio files by calling `_json_download()` on each downloader.

---

## Requirements

- Python 3.10+
- Required libraries:
  - `requests` (or the library used in your downloader classes)
  - `logging` (included in the standard library)
- Access to processed JSONL datasets:
  - `sentences_processed.jsonl`
  - `words_processed.jsonl`
- Internet connection for downloading audio files from Tatoeba.

---

## Usage

1. Ensure your JSONL datasets are available at the specified paths.
2. Set the desired local directories for downloaded audio files.
3. Run the script:

```bash
python3 test.py
