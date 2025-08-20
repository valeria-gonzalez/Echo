# README – `test.py`

## Description

`test.py` is the main script designed to **calculate and update the duration of audio files** for sentences, words, and texts, then send this information to API endpoints. This script automates the process of extracting audio durations from locally stored files and updating backend resources with the timing data.

The script uses the `ImportAudioDuration` class to handle the extraction and upload of audio durations for all data types.

---

## Features

1. Configures **logging** to track progress and errors.
2. Defines API endpoints for updating audio duration for:
   - Words
   - Sentences
   - Texts
3. Specifies local directories where audio files are stored.
4. Initializes the `ImportAudioDuration` class with the directories and API endpoints.
5. Processes audio files and updates the corresponding API endpoints for:
   - Sentences
   - Words
   - Texts

---

## Requirements

- Python 3.10+
- Required libraries:
  - `requests` (or the library used in your `ImportAudioDuration` class)
  - `logging` (included in the standard library)
- Local API endpoints running on:
  - `http://127.0.0.1:8001/resources/words/audio_duration`
  - `http://127.0.0.1:8001/resources/sentences/audio_duration`
  - `http://127.0.0.1:8001/resources/texts/audio_duration`
- Locally downloaded audio files for:
  - Sentences
  - Words
  - Texts

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
