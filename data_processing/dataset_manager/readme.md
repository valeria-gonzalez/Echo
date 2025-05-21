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
- Adds two key metrics to each content item:
  - Difficulty level: evaluates how challenging the content is
  - Content categories: identifies the top 3 subject categories

## 🛠️ Setup & Usage

The DatasetManager class is designed to work within Echo project structure
with minimal setup:

1. Prerequisites

   - Ensure you have the project structure with the following components:
     - _text_difficulty/text_difficulty.py_ - Contains TextDifficultyEvaluator
     - _texts_by_category/text_category_evaluator_ - Contains TextCategoryEvaluator

2. Dataset files

   - Place your input files in a _datasets/_ directory:
     - _group_1_texts.jsonl_ - Text passages from LibriSpeech
     - _tatoeba_sentences.jsonl_ - Sentences from Tatoeba
     - _words-de02e1507605431abd5d829d7e868af5.jsonl_ - Word definitions

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

- _texts_processed.jsonl_: processed text passages with difficulty and
  categories
- _sentences_processed.jsonl_: processed sentences with difficulty and
  categories
- _words_processed.jsonl_: processed words with difficulty and categories

## ⚙️ How it works

1. Text processing:
   - Formats text (lowercase with capitalized first letter)
   - Evaluates difficulty
   - Determines top 3 content categories
2. Sentence processing:
   - Evaluates sentence difficulty
   - Determines top 3 content categories
3. Word processing
   - Calculates word difficulty
   - Analyzes definitions to determine categories

## 🔗 Dependencies

- text_difficulty: custom module for evaluating text difficulty (thanks vale)
- texts_by_category: custom module for categorizing text content (me, tristan)

📂 Project structure

```text
Echo/
├── data_processing/
│   ├── dataset_manager/
│   │   └── dataset_manager.py
│   ├── text_difficulty/
│   │   └── text_difficulty.py
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
