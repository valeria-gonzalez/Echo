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
  - Difficulty level: evaluates how challenging the content is
  - Content categories: identifies the top 3 subject categories
  - Word count: counts how many words are in the sentences and texts, in the case of words,
  it returns the syllable count.
  - Translation: only for texts, it creates the spanish translation of the text.

## 🛠️ Setup & Usage

The DatasetManager class is designed to work within Echo project structure
with minimal setup:

1. Prerequisites

   - Ensure you have the project structure with the following components:
     - `text_difficulty/text_difficulty.py` - Contains TextDifficultyEvaluator
     - `texts_by_category/text_category_evaluator` - Contains TextCategoryEvaluator

2. Dataset files

   - Place your input files in a _datasets/_ directory:
     - `group_1_texts.jsonl` - Text passages from LibriSpeech
     - `tatoeba_sentences.jsonl` - Sentences from Tatoeba
     - `words_dataset` - Words from Wikiextract (must rename your file to this).

3. Running the manager

```py
from data_processing.dataset_manager.dataset_manager import DatasetManager

# Initialize the manager
manager = DatasetManager()

# Process all datasets
manager.get_final_datasets()
```

4. Output
   Processed files will be saved in the _datasets/processed_datasets/_ directory:

- `texts_processed.jsonl`: processed text passages with difficulty and
  categories
- `sentences_processed.jsonl`: processed sentences with difficulty and
  categories
- `words_processed.jsonl`: processed words with difficulty and categories

## ⚙️ How it works

1. Text processing:
   - Formats text (lowercase with capitalized first letter)
   - Evaluates difficulty
   - Determines top 3 content categories
   - Counts the number of words
   - Translates the text
2. Sentence processing:
   - Evaluates sentence difficulty
   - Determines top 3 content categories
   - Counts the number of words
3. Word processing
   - Calculates word difficulty
   - Analyzes definitions to determine categories
   - Counts the number of syllables

## 🔗 Dependencies

- `TextDifficultyEvaluator`: custom module for evaluating text difficulty (thanks vale)
- `TextCategoryEvaluator`: custom module for categorizing text content (me, tristan)
- `TextTranslator`: custom module for translating texts

📂 Project structure

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
