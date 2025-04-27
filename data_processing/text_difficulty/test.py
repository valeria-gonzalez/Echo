from text_difficulty import TextDifficultyEvaluator

def main():
    text = "I'm not good at multitasking nor running, but I can swim."
    word = "dog"
    
    evaluator = TextDifficultyEvaluator()
    print(f"word: {evaluator.word_difficulty(word)}")
    print(f"sentence: {evaluator.sentence_difficulty(text)}")

if __name__ == "__main__":
    main()
    