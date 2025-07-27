# 📁 Speech evaluation

## 📚 Objective
Use the Praat model to analyze various charachteristics of audio files such as:
- gender recognition
- speech mood
- speech rate
- articulation rate
- number of syllables
- count number of pauses
- speaking time

## 📂 Module description
This module is obtained from the project "My-Voice Analysis" created by Shahabks, 
that can be found at the following [Github Repository](https://github.com/Shahabks/my-voice-analysis).

> My-Voice Analysis is a Python library for the analysis of voice (simultaneous speech, high entropy) without the need of a transcription. It breaks utterances and detects syllable boundaries, fundamental frequency contours, and formants. Its built-in functions recognise and measure: gender recognition, speech mood (semantic analysis), pronunciation posterior score, articulation-rate, speech rate, filler words, and f0 statistics.

Thanks to this project, we can readapt the already created functions to use in our
project. 

## ⚙️⚙️ Requirements

### 🔧 Installation

- Python 3.7+

Install the required dependencies:

```bash
pip install os
pip install praat-parselmouth
pip install numpy
pip install scipy
```

These modules can be installed individually or via the `requirements.txt` file located in the root directory. As a disclaimer, it will also install all the required modules needed for preprocessing words, sentences and texts.

To install using the `requirements.txt`use:

```bash
pip install -r requirements.txt
```

### 🗄️ Required files

 In order to use this module, please make sure you have the following file, 
 although it will be included.

 Needed files:
 - `myspsolution.praat`

## 🚀 Usage
```python
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

    # Run all analysis at once
    full_overview = analyzer.get_overview(audio_name, audio_dir)
```

### Function descriptions
- `get_gender_and_mood`: Recognize gender and mood of speech.
- `get_syllable_count`: Detect and count number of syllables.
- `get_pauses_count`: Detect and count number of pauses and fillers.
- `get_rate_of_speech`: Measure the total number of syllables spoken per second (including pauses and fillers).
- `get_articulation_rate`: Measure the total number of syllables spoken per second (excluding pauses and fillers).
- `get_speaking_time`: Measure speaking time (excluding fillers and pauses).
- `get_total_speaking_time`: Measure speaking time (including fillers and pauses).
- `get_speaking_to_total_time_ratio`: Measure ratio between speaking duration and total speaking duration.
- `get_overview`: Get total overview of audio properties. Includes number of syllables, number of pauses, rate of speech, articulation rate, speaking duration, original duration and ratio.

#### Example output of `overview`
```json
{
    'number_of_syllables': 13, 
    'number_of_pauses': 0, 
    'speech_rate': 3.0, 
    'articulation_rate': 5.0,
    'speaking_duration': 2.7,
    'total_duration': 4.6,
    'ratio': 0.6
}
```