# README – `test.py`

## Description

`test.py` is the main script designed to **evaluate audio files of sentences, words, and texts** and upload the evaluation results to API endpoints. This script automates the process of analyzing audio quality or correctness, then updating backend resources with the evaluation data.

The script uses three specialized evaluation classes:

- **ImportEvaluationSentences**: Evaluates sentence audio files and updates the API.
- **ImportEvaluationWords**: Evaluates word audio files and updates the API.
- **ImportEvaluationTexts**: Evaluates text audio files organized by chapters and updates the API.

---

## Features

1. Configures **logging** to track evaluation progress and errors.
2. Sets an evaluation API endpoint for audio analysis.
3. Defines API endpoints for updating evaluation results for:
   - Words
   - Sentences
   - Texts
4. Specifies local directories where audio files are stored.
5. Initializes evaluation classes for sentences, words, and texts.
6. Retrieves evaluation results and uploads them to the corresponding API endpoints.
7. Supports chapter-based evaluation for text audio files.

---

## Requirements

- Python 3.10+
- Required libraries:
  - `requests` (or the library used in your evaluation classes)
  - `logging` (included in the standard library)
- Local API endpoints running on:
  - `http://127.0.0.1:8000/evaluation/analyze_audio` (for evaluation)
  - `http://127.0.0.1:8001/resources/words/evaluation`
  - `http://127.0.0.1:8001/resources/sentences/evaluation`
  - `http://127.0.0.1:8001/resources/texts/evaluation`
- Locally downloaded audio files for:
  - Sentences
  - Words
  - Texts

---

## Usage

1. Ensure your evaluation API and resource APIs are running locally.
2. Place your audio files in the specified directories:
   - `audio_direction_sentences`
   - `audio_direction_words`
   - `direction_texts_audio`
3. Run the script:

```bash
python3 test.py


