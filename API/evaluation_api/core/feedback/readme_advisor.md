# 🧠 Speech Advisor

## 📚 Objective

The `SpeechAdvisor` class uses a Large Language Model (LLM) hosted on a web server to provide friendly, structured feedback on a user's speech performance compared to a reference. By analyzing timing, rhythm, and transcription accuracy, it generates helpful coaching tips tailored to the speaker's performance.

## ✨ Overview

By using the Qwen3-14B Model that can be found at [Arli AI API](https://www.arliai.com/) to prompt a fine-tuned LLM, `Speech Advisor` automatically generates feedback on:

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
pip install requests
pip install json
pip install dotenv
```
#### 2. **Configure the `.env` and `config.py` files**

Create a copy of the `.env.example` file with:

```bash
cp .env.example .env
```

Modify the `.env` file by replacing the variable `ARLI_API_KEY` with the API key 
that [Arli AI](https://www.arliai.com/) provides for **text generation models**.

#### 3. Modify ARLI API key parameters

Also please modify in the ARLI API key parameters the following:
- Select the Qwen3-14B-ArliAI-RpR-v5-Small as the only **model**.
- Mark the **hide thinking** checkbox to stop the model from sharing it's thought process.
- Click **save**.

The parameters that have been modified and applied will have a blue circle next to them.

More information on the different configurations that can be established can be found 
at the 
[Arli Text Generation API Documentation](https://www.arliai.com/docs?lang=en&_gl=1*5wid9d*_up*MQ..*_ga*MzY2ODIwNjcxLjE3NTM1NjQ3Nzk.*_ga_7X1GX4PZG5*czE3NTM1NjQ3NzgkbzEkZzEkdDE3NTM1NjQ3OTEkajQ3JGwwJGgw). 

## 🚀 Usage
```python
from advisor import SpeechAdvisor

advisor = SpeechAdvisor()

difference = {
    "number_of_syllables": -2,
    "number_of_pauses": 1,
    "speech_rate": -0.4,
    "articulation_rate": -0.2,
    "speaking_duration": -0.3,
    "total_duration": 0.2,
    "ratio": -0.15
}

wer = 0.23  # Word Error Rate between user and reference

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

- `get_feedback`: Returns a dictionary with four categories of tips: 
  - speed_tip
  - clarity_tip
  - articulation_tip
  - rythm_tip

- `create_prompt`: Generates a prompt formatted to elicit structured coaching feedback from the LLM.

- `make_api_request`: Sends the prompt to the Arli AI API and parses the returned JSON. Includes schema enforcement and fallback handling.

- `load_api_key`: Loads the API key from a separate configuration file (config.py).

## 📦 Prompt Design Guidelines
The generated prompt:
- Requests JSON output
- Encourages warm, encouraging language
- Adapts tone based on severity of speech differences
- Prohibits technical terms (like “WER” or “speech rate”) in the feedback itself

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