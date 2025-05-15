# Text Category Evaluator

This Python project uses a zero-shot learning approach to classify a given text into predefined lifestyle-related categories using the Hugging Face transformers library and the facebook/bart-large-mnli model.

## 🔍 Overview

The TextCategoryEvaluator class evaluates a given text and estimates its relevance across six predefined categories:

- Daily Life

- Work

- Social Life

- Education

- Travel

- Health

It leverages a zero-shot classification model to assign confidence scores to each category based on the input text.

## 🚀 Installation

_1._ Clone the repository or copy the code
_2._ Install the required Python libraries:

```text
    pip install transformers
    pip install torch
```

## 🧠 How It Works

The classifier uses the _"facebook/bart-large-mnli"_ model to perform zero-shot
classification. Given a string of text, it compares the content against
category descriptions and returns a probability score for each.

## 📦 Usage

```py
    from your_module import TextCategoryEvaluator  # Replace with actual filename if saved

    evaluator = TextCategoryEvaluator()

    text = "I visited Paris and enjoyed the food and museums."
    results = evaluator.classify_words(text)

    for category, score in results.items():
        print(f"Category: [{category}], Score: [{score:.2%}]")

```

## ✅ Example Output

```text
Category: [travel], Score: [94.20%]
Category: [social life], Score: [2.85%]
Category: [daily life], Score: [1.94%]
...

```

## 📁 Class Structure

TextCategoryEvaluator

- **init**()
  Loads the zero-shot model and defines the category labels.

- classify_words(text_data: str) -> dict
  Takes a string input and returns a dictionary with categories and their confidence scores.

## 🛠️ Customization

You can edit the self.category_labels dictionary inside the class to add, remove, or redefine categories based on your use case.

## 📋 License

This project is for educational and research purposes. The model used
(facebook/bart-large-mnli) is provided by Meta via the Hugging Face Model Hub.
