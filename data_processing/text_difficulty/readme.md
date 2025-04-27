# Text difficulty

## Objective

Rate the english texts used in the project by difficulty: easy(0), medium(1) and hard(2).

## Getting Started

### 1. Install needed libraries

For this section, the following modules were used:
- textstat
- wordfreq
- big-phoney

These modules can be installed individually or via the `requirements.txt` file located in the root directory. As a disclaimer, it will also install all the required modules needed for preprocessing words, sentences and texts.

To install using the `requirements.txt`use:

```
pip install -r requirements.txt
```

###  3. Example usage

All that's necessary is to call the methods `word_difficulty`, 
`sentence_difficulty` or `text_difficulty` depending on what type of text is 
going to be evaluated.

```
from text_difficulty import TextDifficultyEvaluator

def main():
    sentence = "I'm not good at multitasking nor running, but I can swim."
    word = "dog"
    
    evaluator = TextDifficultyEvaluator()
    print(f"word: {evaluator.word_difficulty(word)}")
    print(f"sentence: {evaluator.sentence_difficulty(sentence)}")

if __name__ == "__main__":
    main()
    
```

#### Result

All of these methods return values between 0 and 2 representing the difficulty,
and make use of external libraries in order to calculate phonemes and syllables. 
Please note that especially sentence and text ratings may take longer to run. 

These methods work in the following way:

- `word_difficulty(word)`: Evaluates the word's difficulty based on amount of
syllables, phonemes and word frequency in the english language.

- `sentence_difficulty(sentence)`: Evaluates the sentences's difficulty based on
amount of syllables, words and the estimated grade level comprehension needed to
understand the sentence.


