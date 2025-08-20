# README – `test.py`

## Description

`test.py` is the main script designed to **import words, sentences, and texts from processed JSONL files into local API endpoints**. This script facilitates bulk data uploads to specific endpoints, keeping a backend updated with structured information automatically.

The script uses three specialized import classes:

- **ImportWords**: Sends word entries to the words API endpoint.
- **ImportSentences**: Sends sentence entries to the sentences API endpoint.
- **ImportTexts**: Sends text entries to the texts API endpoint.

It is expected that the endpoints are running locally, e.g., with Uvicorn or FastAPI.

---

## Features

1. Configures **logging** to track the import process and errors.
2. Defines API endpoint URLs for each data type:
    - Words
    - Sentences
    - Texts
3. Specifies paths to the processed JSONL files:
    - `words_processed.jsonl`
    - `sentences_processed.jsonl`
    - `texts_processed.jsonl`
4. Initializes the import classes and executes the data import automatically.

---

## Requirements

- Python 3.10+
- Required libraries:
  - `requests` (or whatever your import classes use to make HTTP requests)
  - `logging` (included in the standard library)
- Local servers running on:
  - `http://127.0.0.1:8001/resources/words`
  - `http://127.0.0.1:8001/resources/sentences`
  - `http://127.0.0.1:8001/resources/texts`
- Processed dataset JSONL files.

---

## Usage

1. Ensure your local APIs are running.
2. Place the JSONL files in the specified paths.
3. Run the script:

```bash
python3 test.py