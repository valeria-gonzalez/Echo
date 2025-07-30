
# Import JSONLs to Firebase
The project is designed to import data from JSONL files into to google firebase. 🔍

## ⚠️ IMPORTANT NOTICE ⚠️
Before runnig any import scripts, make sure:
-1 The API server is up and running
-2 All Tatoeba and corpus audio files download

## project structure 📦

Ensure the following directory structure is in place
```
    \---data_import
        ├── data_download
        │   ├── audios
        │   ├── download_sentences.py
        │   └── test.py
        ├── import_audio_sentences.py
        ├── import_audio_texts.py
        ├── import_sentences.py
        ├── import_texts.py
        ├── import_words.py
        ├── readme.md
        ├── requirements.txt
        └── test.py

    \---data_processing
        +---dataset_manager
        |   |
        |   \---processed_datasets
        |           sentences_processed.jsonl
        |           texts_processed.jsonl
        |           words_processed.jsonl

```

## ⚙️ Requirements ⚙️

### 🔧 Installation

- Python 3.7+

Install the required dependencies:

```bash
pip install requests
pip install jsonlines

```

alternatively, you can install all dependencies using the requeriments.txt file:

```bash
pip install -r requirements.txt
```

### 🗄️ Required files 🗄️
Make sure the following processed .jsonl files are available in the path:

- `sentences_processed.jsonl`
- `texts_processed.jsonl`
- `words_processed.jsonl`

## 🧠 How It Works

📦 Import Scripts

Each of the following scripts is responsible for importing a specific type of data by sending it to the corresponding API using POST requests. The data can come from either JSONL files or audio files.

Script	Description

`import_words.py`	Imports word data from JSONL files
`import_sentences.py`	Imports sentence data from JSONL
`import_texts.py	Imports` text data from JSONL
`import_audio_sentences.py`	Uploads sentence audio files
`import_audio_texts.py`	Uploads text audio files

All scripts use HTTP POST requests to send the data to their respective API endpoints.

## 🚀 Run the test.py 🚀
the `test.py` script import data from procedded JSONL files and sends it to corresponding API endpoints.

It import words, sentences and texts using the JSONLs by creating instances `importWords`, `importSentences` ,`importTexts`, `importAudioSentences` and `importAudioTexts`


🌐 API Endpoints & File Paths

    ⚠️ Important: Make sure to update the endpoints if the APIs are deployed on a different server, port, or domain.

The following are the default local endpoints and the corresponding file paths used by the import scripts:
🔤 Words

    API Endpoint:
    http://127.0.0.1:8000/resources/words

    JSONL File Path:
    ../data_processing/dataset_manager/processed_datasets/words_processed.jsonl

📝 Sentences

    API Endpoint:
    http://127.0.0.1:8000/resources/sentences

    JSONL File Path:
    ../data_processing/dataset_manager/processed_datasets/sentences_processed.jsonl

📚 Texts

    API Endpoint:
    http://127.0.0.1:8000/resources/texts

    JSONL File Path:
    ../data_processing/dataset_manager/processed_datasets/texts_processed.jsonl

🔊 Sentence Audios

    API Endpoint:
    http://127.0.0.1:8000/resources/sentences/audios

    Audio Directory:
    ./data_download/audios

🔉 Text Audios

    API Endpoint:
    http://127.0.0.1:8000/resources/texts/audios

    Audio Directory:
    ../data_processing/texts/datasets/chapters/group_1_audios


