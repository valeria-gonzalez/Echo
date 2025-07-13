import os
from evaluation.evaluator import SpeechEvaluator

def main():
    # Define audio file details
    audio_dir = os.getcwd()
    evaluator = SpeechEvaluator()
    
    # Get analysis score
    score = evaluator.get_analysis("audioval", "audio5", audio_dir)
    # Print scores
    print("================= SCORE ====================")
    for key, value in score.items():
        print(f"{key} : {value}")
    print()
        
    # Get feedback
    feedback = evaluator.get_feedback("audioval", "audio5", audio_dir)
    # Print feedback
    print("============== FEEDBACK ===================")
    for key, value in feedback.items():
        print(f"{key} : ")
        for item in value:
            print(f"  - {item}")
        print()
    
    
if __name__ == "__main__":
    main()
