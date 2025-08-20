# Audio and Data Import and Management Project

This project is designed to handle the downloading, importing, and analysis of audios, words, sentences, and texts for later use in evaluations and audio duration storage. It is divided into several folders according to the functionality of each module.

## Folder Structure

├── download_audios
│ ├── audios_sentences
│ ├── audios_words
│ ├── download_sentences.py
│ ├── download_words.py
│ ├── readme.md
│ └── test.py
├── import_audio_duration
│ ├── import_audio_duration.py
│ ├── readme.md
│ └── test.py
├── import_audios
│ ├── import_audio_sentences.py
│ ├── import_audio_texts.py
│ ├── import_audio_words.py
│ ├── readme.md
│ └── test.py
├── import_evaluation
│ ├── import_evaluation_sentences.py
│ ├── import_evaluation_texts.py
│ ├── import_evaluation_words.py
│ ├── readme.md
│ └── test.py
├── import_jsonl
│ ├── import_sentences.py
│ ├── import_texts.py
│ ├── import_words.py
│ ├── readme.md
│ └── test.py
├── readme.md


## Execution Flow

To ensure the data is processed correctly, the modules must be run in the following order:

1. **`import_jsonl`**  
   - This module imports words, sentences, and texts from JSONL files to the API endpoints.
   - Run `test.py` in this folder to start the import.

2. **`download_audios`**  
   - Downloads audios for words and sentences and organizes them into the `audios_words` and `audios_sentences` folders.
   - Run `test.py` in this folder to download the audios.

3. **`import_audios`**  
   - Imports the downloaded audios into the corresponding API endpoints.
   - Run `test.py` in this folder after downloading the audios.

4. **`import_evaluation`**  
   - Imports evaluation data associated with words, sentences, and texts.
   - Run `test.py` in this folder after importing the audios.

5. **`import_audio_duration`**  
   - Calculates and updates the duration of each audio in the database or API.
   - Run `test.py` in this folder at the end of the workflow.

## Notes

- Each folder contains its own `readme.md` with specific details about its functionality.
- The `test.py` scripts serve as entry points to run each module independently.
- Make sure the API is running before executing modules that interact with it.
- This project is designed to be executed in the order listed to avoid data dependency errors.

## Requirements

- Python 3.10 or higher.
- Required libraries are defined in each script or can be consolidated in a general `requirements.txt`.
- Access to the corresponding API for data import.

## Example of Execution

```bash
# Step 1: Import JSONL data
python import_jsonl/test.py

# Step 2: Download audios
python download_audios/test.py

# Step 3: Import downloaded audios
python import_audios/test.py

# Step 4: Import evaluation data
python import_evaluation/test.py

# Step 5: Update audio durations
python import_audio_duration/test.py


