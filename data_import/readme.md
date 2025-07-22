
# Import JSONLs 
The project aims to import data from JSONL files into to google firebase. 🔍

## ⚠️ IMPORTANT NOTICE ⚠️
Before running the import scripts, make sure that the corresponding API is up and running.

## project structure 📦

We need the following directory structure to properly run the project
```
\---Echo
    |
    |data_import
    |    import_sentences.py
    |    import_texts.py
    |    import_words.py
    |    readme.md
    |    requirements.txt
    |    test.py
    |
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

### 🗄️ Required files
The files we needed are the following:

Needed file:

- `sentences_processed.jsonl`
- `texts_processed.jsonl`
- `words_processed.jsonl`

## 🧠 How It Works

Each class takes a corresponding JSONL file, trasforms each JSONL line into different json object, and sends it via post request to the provided API endpoint

## 🚀 Run the test.py 🚀
the `test.py` script import data from procedded JSONL files and sends it to corresponding API endpoints.

It import words, sentences and texts using the JSONLs by creating instances `importWords`, `importSentences` and `importTexts`

### the endpoints used
make sure to update the endpoints when the APIs are deployed to a different server o domain
- words = "http://127.0.0.1:8000/resources/words"
- sentences = "http://127.0.0.1:8000/resources/sentences"
- texts = "http://127.0.0.1:8000/resources/texts"

