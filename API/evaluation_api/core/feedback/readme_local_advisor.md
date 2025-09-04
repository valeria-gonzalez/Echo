# 🧠 Local Speech Advisor

## 📚 Objective

The `LocalSpeechAdvisor` class uses a locally hosted LLM model to provide friendly, structured speech coaching feedback. By analyzing timing, clarity, rhythm, and articulation, it generates warm, personalized suggestions for improving pronunciation and delivery — completely offline.

## ✨ Overview

By using the  Mistral-7B Model that can be found at [Hugging Face](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF) to prompt a fine-tuned LLM, `Local Speech Advisor` automatically generates feedback on:

- **Clarity**: Word accuracy and syllable match.
- **Speed**: Speech rate and durations.
- **Articulation**: Syllables and articulation rate.
- **Rhythm**: Pauses and timing consistency.

It will return three tips for each category with:
- One assesment of the speaker's performance compared to the reference.
- One tip on how to improve.
- One tip on how to improve in the future.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+

### Installation

#### 1. **Install dependencies**

```bash
pip install llama-cpp-python
pip install os
pip install json
```
#### 2. **Download model file**

In order for the class to work, the `.gguf` file containing the model must be downloaded from [Hugging Face](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF). 

Please download the file named `mistral-7b-instruct-v0.1.Q4_K_M.gguf` from the website and place it inside a directory named `models` with this exact name.

## 🚀 Usage
```python
from local_advisor import LocalSpeechAdvisor

advisor = LocalSpeechAdvisor()

difference = {
    "number_of_syllables": -2,
    "number_of_pauses": 1,
    "speech_rate": -0.4,
    "articulation_rate": -0.2,
    "speaking_duration": -0.3,
    "total_duration": 0.2,
    "ratio": -0.15
}

wer = 0.18  # Word Error Rate between user and reference

feedback = advisor.get_feedback(difference, wer)

print(feedback)
```

### Example Output
```json
{
    "clarity_tip": [
        "Your pronunciation is clear, but there are some small differences compared to the original audio. Listen carefully to yourself and pay attention to any mistakes you make.",
        "You could benefit from practicing listening exercises that focus on clarity.",
        "Consider recording yourself speaking and comparing your delivery to the original audio."
    ],
    "speed_tip": [
        "You spoke at a very similar pace to the original audio. Keep up the good work!",
        "Try practicing speaking with more pauses in between sentences.",
        "Practice speaking slowly and deliberately."
    ],
    "rythm_tip": [
        "Your rhythm is very similar to the original audio. Keep up the good work!",
        "Try practicing speaking with more pauses in between sentences.",
        "Practice speaking slowly and deliberately."
    ],
    "articulation_tip": [
        "Your articulation rate is quite high, which can sometimes lead to confusion. Try focusing on enunciating each word clearly.",
        "Practice speaking with a slower pace to give yourself more time to think about how you're pronouncing words.",
        "Consider practicing tongue twisters or other exercises that challenge your ability to articulate sounds."
    ]
}
```

## Class Overview
- `get_feedback`: Returns coaching tips based on analysis differences and WER.
- `create_prompt`: Generates the full user-friendly prompt for the model.
- `generate_output`: Handles token generation using the local llama.cpp model.
- `parse_response`: Cleans and parses model output into a valid dictionary.

## Fallback
If the API fails or returns an invalid response, the class will gracefully return fallback responses like:

```json
{
  "speed_tip": ["We're sorry, no feedback was generated."],
  "clarity_tip": ["Please try again later."],
  "articulation_tip": [],
  "rythm_tip": []
}
```