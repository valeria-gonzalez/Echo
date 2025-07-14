# 📊 Dataset Manager - README

## 🔍 Overview

DatasetManager is a text processing utility for evaluating the difficulty and
categorizing different types of English content. It processes text passages,
sentences, and individual words, enhancing them with metadata about
difficulty levels and content categories.

## ⚡ Features

- Processes three types of content:
  - Full texts/passages (from LibriSpeech)
  - Sentences (from Tatoeba database)
  - Individual words (with definitions)

- Adds four key metrics to each content item:
  - **Difficulty level**: Evaluates how challenging the content is
  - **Content categories**: Identifies the top 3 subject categories
  - **Word count**: Counts how many words are in the sentences and texts.
  - **Translation**: Only for texts, it creates the spanish translation of the text.
  - **Syllable count**: Counts hoy many syllables are in a word.

## 🛠️ Setup & Usage

The DatasetManager class is designed to work within Echo project structure
with minimal setup:

### 1. Prerequisites

   - Ensure you have the project structure with the following components:
     - `text_difficulty/text_difficulty.py` - Contains TextDifficultyEvaluator
     - `texts_by_category/text_category_evaluator` - Contains TextCategoryEvaluator

### 2. Dataset files

   - Place your input files in a _datasets/_ directory:
     - `group_1_texts.jsonl` - Text passages from LibriSpeech
     - `tatoeba_sentences.jsonl` - Sentences from Tatoeba
     - `words_dataset` - Words from Wikiextract (must rename your file to this).

### 3. Running the manager

```python
from data_processing.dataset_manager.dataset_manager import DatasetManager

# Initialize the manager
manager = DatasetManager()

# Process all datasets
manager.get_final_datasets()
```

### 4. Output
   Processed files will be saved in the _datasets/processed_datasets/_ directory:

- `texts_processed.jsonl`: processed text passages with difficulty and
  categories
- `sentences_processed.jsonl`: processed sentences with difficulty and
  categories
- `words_processed.jsonl`: processed words with difficulty and categories

### JSON output

#### Word example JSON
```JSON
[
    {
        "word": "dictionary", 
        "definitions": 
        [
            {
                "pos": "noun", 
                "definitions": 
                [
                    "An associative array, a data structure where each value is referenced by a particular key, analogous..", 
                    "A synchronic dictionary of a standardised language held to only contain words that are properly part..", 
                    "A reference work with a list of words from one or more languages, normally ordered alphabetically..", 
                    "Any work that has a list of material organized alphabetically; e.g., biographical dictionary.."
                ]
            }, 
            {
                "pos": "verb", 
                "definitions": 
                [
                    "To look up in a dictionary.", 
                    "To add to a dictionary.", 
                    "To compile a dictionary."
                ]
            }
        ], 
        "ipa": "/\u02c8d\u026ak.\u0283\u0259.n\u0259.\u0279i/", 
        "mp3_url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/1/1f/En-uk-dictionary.ogg/En-uk-dictionary.ogg.mp3", 
        "translations": ["diccionario"],
        "difficulty": 1, 
        "categories": ["education", "work", "travel"], 
        "syllable_count": 4
    }
]
```

#### Text example JSON
```JSON
[
    {
        "chapter_id": "141231", 
        "book_title": "Planet of the Damned - (Chapter 01)", 
        "transcript": 
        {
            "audio_file": "segment_0.flac", 
            "duration": 11.19, 
            "text_lines": 
            [
                "1272-141231-0000 [0.00s - 4.65s]: A MAN SAID TO THE UNIVERSE SIR I EXIST", 
                "1272-141231-0001 [4.65s - 11.19s]: SWEAT COVERED BRION'S BODY TRICKLING INTO THE TIGHT LOINCLOTH THAT WAS THE ONLY GARMENT HE WORE"
            ], 
            "full_text": "A man said to the universe sir i exist sweat covered brion's body trickling into the tight loincloth that was the only garment he wore"
        }, 
        "difficulty": 0, 
        "word_count": 25, 
        "categories": ["health", "education", "work"], 
        "translation": "Un hombre dijo al universo se\u00f1or que existo sudor cubri\u00f3 el cuerpo de Brion tocando el lomo apretado que era la \u00fanica prenda que usaba"
    }
]
```

#### Sentence example JSON
```JSON
[
    {
        "eng_sen": "If I could rearrange the alphabet, I would put U and I together.", 
        "spa_sen": "Si pudiera reordenar el alfabeto, pondr\u00eda la T y la Q juntas.", 
        "audio_id": 1123747, 
        "difficulty": 2, 
        "categories": ["health", "work", "education"], 
        "word_count": 13
    }
]
```


## ⚙️ How it works

### 1. Text processing:
   - Formats text (lowercase with capitalized first letter)
   - Evaluates difficulty
   - Determines top 3 content categories
   - Counts the number of words
   - Translates the text

### 2. Sentence processing:
   - Evaluates sentence difficulty
   - Determines top 3 content categories
   - Counts the number of words

### 3. Word processing
   - Calculates word difficulty
   - Analyzes definitions to determine categories
   - Counts the number of syllables

## 🔗 Dependencies

- `TextDifficultyEvaluator`: custom module for evaluating text difficulty (thanks vale)
- `TextCategoryEvaluator`: custom module for categorizing text content (me, tristan)
- `TextTranslator`: custom module for translating texts

### 📂 Project structure

```text
Echo/
├── data_processing/
│   ├── dataset_manager/
│   │   └── dataset_manager.py
│   ├── text_difficulty/
│   │   └── text_difficulty.py
│   ├── text_translate/
│   │   └── text_translate.py
│   └── texts_by_category/
│       └── text_category_evaluator.py
└── datasets/
    ├── group_1_texts.jsonl
    ├── tatoeba_sentences.jsonl
    └── words-de02e1507605431abd5d829d7e868af5.jsonl
```

## 💡 Notes

- Make sure your input files follow the expected format
- The difficulty levels are determined based on linguistic complexity metrics
- Categories are extracted using NLP classification techniques
- The translations are obtained with open source APIs, which depending on the chosen one,
might need to be locally hosted.
