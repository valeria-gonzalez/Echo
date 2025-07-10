from speech_analyzer import SpeechAnalyzer
import os

# Define audio file details
audio_name = "audio5"
audio_dir = os.getcwd()

# Initialize the analyzer
analyzer = SpeechAnalyzer()

# Run all analyses
gender_mood = analyzer.get_gender_and_mood(audio_name, audio_dir)
syllable_count = analyzer.get_syllable_count(audio_name, audio_dir)
pause_count = analyzer.get_pauses_count(audio_name, audio_dir)
speech_rate = analyzer.get_rate_of_speech(audio_name, audio_dir)
articulation_rate = analyzer.get_articulation_rate(audio_name, audio_dir)
speaking_time = analyzer.get_speaking_time(audio_name, audio_dir)
total_time = analyzer.get_total_speaking_time(audio_name, audio_dir)
speaking_ratio = analyzer.get_speaking_to_total_time_ratio(audio_name, audio_dir)
full_overview = analyzer.get_overview(audio_name, audio_dir)

# Display results
print("=== Speech Analysis Results ===")
print(f"Gender & Mood: {gender_mood}")
print(f"Syllable Count: {syllable_count}")
print(f"Pause Count: {pause_count}")
print(f"Rate of Speech: {speech_rate} syllables/sec")
print(f"Articulation Rate: {articulation_rate} syllables/sec")
print(f"Speaking Time (excl. pauses): {speaking_time} sec")
print(f"Total Speaking Time: {total_time} sec")
print(f"Speaking-to-Total Time Ratio: {speaking_ratio:.2f}")
print(f"\nFull Overview:\n{full_overview}")
