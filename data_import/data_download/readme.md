# TATOEBA SENTENCES AUDIO DOWNLOADER

This script is desing to automatically download audio files for sentences from the [TATOEBA PROJECT](https://tatoeba.org/)

## Project Structure

.
├── audios #Folder where the downloaded .mp3 audio
├── download_sentences.py
├── readme.md
└── test.py #Script theat tuns the download processs

## Requirements
- Python 3.7+
- Internet connection (to access Tatoeba.org)

### Install dependencies

```bash
pip install requests
```

## How to Use

1 - Make sure your JSON file is in the correct path
2 - run the script

```bash
python3 test.py
```

### features
- Download audio from tatoeba
- saves as .mp3 with the name <audio_id>.mp3
- Automaticallt creates the destination folder
- Logs download status (success or error) to the console

## Example
AUDIO DOWNLOADED SUCCESSFULLY: 0
AUDIO DOWNLOADED SUCCESSFULLY: 1
AUDIO DOWNLOADED SUCCESSFULLY: 2

