from text_difficulty import TextDifficultyEvaluator
import warnings
import json
import textstat
import syllables
from collections import Counter


    
def get_avg_text():
    evaluator = TextDifficultyEvaluator()
    with open('../texts/datasets/chapters/group_1_texts.jsonl') as f:
        obj = json.load(f)
        wrd_cnt = []
        syl_cnt = []
        dif_cnt = []
        for i,entry in enumerate(obj):
            text = entry.get("transcript").get("full_text")
            text = text.lower()
            words = textstat.lexicon_count(text, removepunct=True)
            syl = syllables.estimate(text)
            grade = textstat.dale_chall_readability_score(text)
            print("\n------------------------------------------------------")
            print(f"Text: {text}")
            print(f"Grade: {round(grade)}")
            print(f"Words: {words}")
            print(f"Syl: {syl}")
            print(f"Calculated dif: {evaluator.text_difficulty(text)}")
            wrd_cnt.append(words)
            syl_cnt.append(syl)
            dif_cnt.append(round(grade))
            
        counter_syl = Counter(syl_cnt)
        mode_syl = max(counter_syl, key=counter_syl.get)
        counter_wrd = Counter(wrd_cnt)
        mode_wrd = max(counter_wrd, key=counter_wrd.get)
        counter_dif = Counter(dif_cnt)
        mode_dif = max(counter_dif, key=counter_dif.get)
        
        print("\n------------------------------------------------------")
        print(f"avg syl: {sum(syl_cnt)/len(syl_cnt)}")
        print(f"mx syl: {max(syl_cnt)}")
        print(f"mode syl: {mode_syl}\n")
        print(f"avg wrd: {sum(wrd_cnt)/len(syl_cnt)}")
        print(f"mx wrd: {max(wrd_cnt)}")   
        print(f"mode wrd: {mode_wrd}\n")
        print(f"avg dif: {sum(dif_cnt)/len(dif_cnt)}")
        print(f"mx dif: {max(dif_cnt)}")   
        print(f"mode dif: {mode_dif}")

def main():
    ignore_warnings()
    
    sentence = "I'm not good at multitasking nor running, but I can swim."
    word = "dog"
    text = (
        "A MAN SAID TO THE UNIVERSE SIR I EXIST SWEAT COVERED BRION'S BODY "
        "TRICKLING INTO THE TIGHT LOINCLOTH THAT WAS THE ONLY GARMENT HE WORE"
    )
    
    evaluator = TextDifficultyEvaluator()
    #print(f"word difficulty: {evaluator.word_difficulty(word)}")
    #print(f"sentence difficulty: {evaluator.sentence_difficulty(sentence)}")
    #print(f"text difficulty: {evaluator.text_difficulty(text)}")  
    get_avg_text()

if __name__ == "__main__":
    main()
    