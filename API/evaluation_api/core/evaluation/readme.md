# 📁 Speech Scoring & Evaluation

## 📚 Objective

This module provides an evaluation system for speech analysis by comparing a user's audio to a reference audio using both objective metrics (e.g., speech rate, articulation) and a transcription-based word error rate. The result is a scoring system across clarity, speed, articulation, and rhythm.

## 📂 Module description

This evaluator is designed to complement audio analysis tools like the ones found in the [My-Voice Analysis project](https://github.com/Shahabks/my-voice-analysis), by providing a **quantitative scoring mechanism**. It allows you to evaluate pronunciation accuracy and fluency using precomputed analysis dictionaries for both the user and the reference audio.

The scoring is based on:
- **Clarity score:** Scored over 10 points, it considers the Word Error Rate of the two transcripts and the number of syllables. 
- **Speed Score:** Scored over 10 points, it considers the speech rate, speaking duration and total duration.
- **Articulation score:** Scored over 10 points, it considers the articulation rate and the number of syllables.
- **Rythm score:** Scored over 10 points, it considers speaking-to-total-time ratio and the number of pauses.
- **Total score:** Scored over 100% points, it is the sum of all the evaluation points scored over 100%.

## ⚙️ Requirements

### 🔧 Installation

Make sure to have Python 3.8+ and install the required dependencies:

```bash
pip install jiwer
```

The jiwer library is used to compute Word Error Rate (WER) between reference and predicted transcriptions.


## 🚀 Usage
```python
from evaluator import SpeechEvaluator

evaluator = SpeechEvaluator()

# Example user and reference analysis dictionaries
reference = {
    "transcription": "hello this is a test",
    "number_of_syllables": 6,
    "number_of_pauses": 1,
    "speech_rate": 3.5,
    "articulation_rate": 4.2,
    "speaking_duration": 2.4,
    "total_duration": 3.2,
    "ratio": 0.75
}

user = {
    "transcription": "hello this test",
    "number_of_syllables": 5,
    "number_of_pauses": 2,
    "speech_rate": 3.2,
    "articulation_rate": 4.0,
    "speaking_duration": 2.1,
    "total_duration": 3.4,
    "ratio": 0.62
}

# Get evaluation score
score = evaluator.get_score(user, reference)

# Get difference in analysis
diff = evaluator.get_difference_analysis(user, reference)

print(score)
print(diff)
```

### 🧮 Function descriptions
- `compare_transcripts` : Compare reference and predicted transcriptions using Word Error Rate (WER) with a tolerance margin.

- `get_analysis_score` : Compute scores per category (clarity, speed, articulation, rhythm). Each category is scored out of 10, with a final normalized total score out of 100.

- `get_score` : Public method to return the full breakdown of scores:
  - clarity_score
  - speed_score
  - articulation_score
  - rythm_score
  - total_score

- `get_difference_analysis` : Returns a dictionary of relative differences (value between 0 and 1) between user and reference values for analysis keys such as:
    - **Speech rate:** Total number of syllables spoken per second (including pauses and fillers).
    - **Articulation rate:** Total number of syllables spoken per second (excluding pauses and fillers).
    - **Number of syllables:** Number of syllables spoken.
    - **Count number of pauses:** Number of pauses and fillers.
    - **Speaking time:** Speaking time (excluding fillers and pauses).
    - **Total speaking time:** Speaking time (including fillers and pauses).
    - **Speaking to Total Time Ratio:** Ratio between speaking duration and total speaking duration.

    Values closer to zero mean more similarity and closer to one mean dissimilarity.

### 🧪 Example output of `get_score`
```json
{
    "clarity_score": 8,
    "speed_score": 9,
    "articulation_score": 8,
    "rythm_score": 7,
    "total_score": 80
}
```
### 🧮 Example output of `get_difference_analysis`

The negative values mean the speech was slower and the positive ones mean it was faster.

```json
{
    "number_of_syllables": -1,
    "number_of_pauses": 1,
    "speech_rate": -0.3,
    "articulation_rate": -0.2,
    "speaking_duration": -0.3,
    "total_duration": 0.2,
    "ratio": -0.13
}
```