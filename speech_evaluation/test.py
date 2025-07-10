import os
from analysis.analyzer import SpeechAnalyzer
from transcription.transcriber import SpeechTranscriber
from feedback.advisor import SpeechAdvisor
import utils.audio_tools as atool

def analyze_audio(audio_name:str, audio_dir:str, analyzer, transcriber)-> dict:
    try:
        normalized_audio_name = atool.normalize_audio(audio_name, audio_dir, overwrite=True)
    except FileNotFoundError as e:
        print("Missing file:", e)
    except atool.AudioNormalizationError as e:
        print("Normalization error:", e)
        
    full_overview = analyzer.get_overview(normalized_audio_name, audio_dir)
    transcription = transcriber.get_transcription(normalized_audio_name, audio_dir)
    full_overview["transcription"] = transcription
    return full_overview
    
def main():
    # Define audio file details
    audio_dir = os.getcwd()
    
    # Initialize the analyzer
    analyzer = SpeechAnalyzer()
    
    # Initialize the transcriber
    transcriber = SpeechTranscriber()
    
    evaluator = SpeechAdvisor()
    
    original_overview = analyze_audio("audio5", audio_dir, analyzer, transcriber)
    user_overview = analyze_audio("audioval", audio_dir, analyzer, transcriber)
    error = atool.compare_transcripts(original_overview["transcription"], 
                                          user_overview["transcription"])
    
     # Display results
    print(f"\nOriginal overview:\n{original_overview}\n")
    print(f"User overview:\n{user_overview}\n")
    print(f"Transcription error: {error}\n")
    
    prompt = evaluator._create_prompt(user_overview, original_overview, error)
    print(prompt + "\n\n")
    request = evaluator._make_api_request(prompt)
    
    
if __name__ == "__main__":
    main()
