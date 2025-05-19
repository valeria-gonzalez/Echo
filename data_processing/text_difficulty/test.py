from text_difficulty import TextDifficultyEvaluator
import warnings

def ignore_warnings():
    # Ignore warnings that contain this specific message
    warnings.filterwarnings(
        "ignore",
        message="Argument `input_length` is deprecated",
        category=UserWarning
    )

def main():
    ignore_warnings()
    sentence = "I'm not good at multitasking nor running, but I can swim."
    word = "dog"
    text = ("HE HAD BEEN A CLERK IN A BANKING HOUSE AND WAS TRANSPORTED FOR "
            "EMBEZZLEMENT THOUGH BY SOME GRAVE DOUBTS AS TO HIS GUILT WERE "
            "ENTERTAINED WHEN THE MUSTER BELL RANG AND THE GANG BROKE UP RUFUS "
            "DAWES ON HIS SILENT WAY TO HIS SEPARATE CELL OBSERVED A NOTABLE "
            "CHANGE OF CUSTOM IN THE DISPOSITION OF THE NEW CONVICT I'M NOT TO "
            "GO IN THERE SAYS THE EX BANK CLERK DRAWING BACK IN DISMAY FROM THE "
            "CLOUD OF FOUL FACES WHICH LOWERED UPON HIM"
    )
    text2 = ("THEREAFTER THIS SONNET BRED IN ME DESIRE TO WRITE DOWN IN VERSE "
             "FOUR OTHER THINGS TOUCHING MY CONDITION THE WHICH THINGS IT "
             "SEEMED TO ME THAT I HAD NOT YET MADE MANIFEST WHICH THING BEING "
             "THUS THERE CAME A DAY WHEN CERTAIN LADIES TO WHOM IT WAS WELL "
             "KNOWN THEY HAVING BEEN WITH ME AT DIVERS TIMES IN MY TROUBLE "
             "WERE MET TOGETHER FOR THE PLEASURE OF GENTLE COMPANY BUT WHEN I "
             "STILL SPAKE NOT ONE OF THEM WHO BEFORE HAD BEEN TALKING WITH "
             "ANOTHER ADDRESSED ME BY MY NAME SAYING TO WHAT END LOVEST THOU "
             "THIS LADY SEEING THAT THOU CANST NOT SUPPORT HER PRESENCE"
    )
    
    text3 = ("A PERSON WOULD THINK THAT AFTER A FAMILY HAD LIVED SO LONG IN A "
             "PLACE ALL THE NEIGHBORS WOULD BE FOND OF THEM YET IT IS NOT SO "
             "IT IS DISGRACEFUL THEY THOUGHT THE TROUBLE CAME FROM BAD "
             "BRINGING UP OR NO BRINGING UP AT ALL THEY ALWAYS ATE PLAIN FOOD "
             "AND PLENTY OF IT AND THEY NEVER ATE BETWEEN MEALS"
    )
    
    evaluator = TextDifficultyEvaluator()
    # print(f"word: {evaluator.word_difficulty(word)}")
    # print(f"sentence: {evaluator.sentence_difficulty(sentence)}")
    print(f"text: {evaluator.text_difficulty(text)}")
    print(f"text2: {evaluator.text_difficulty(text2)}")
    print(f"text3: {evaluator.text_difficulty(text3)}")
    

if __name__ == "__main__":
    main()
    