# 🎯 Speech Evaluation & Feedback API

## 📋 Overview

A comprehensive **FastAPI-based microservice** that analyzes English
pronunciation using **Praat acoustic analysis** and
**AI-powered feedback generation**. This API provides detailed voice
quality metrics, personalized recommendations, and practice tips for English
language learners.

## 📚 API Documentation

### 🔗 **Endpoints**

| Method | Endpoint                    | Description                |
| ------ | --------------------------- | -------------------------- |
| `GET`  | `/`                         | Welcome message            |
| `POST` | `/evaluation/analyze_audio` | Analyze speech metrics     |
| `POST` | `/evaluation/evaluate_audio`| Grade speech               |
| `POST` | `/evaluation/feedback`      | AI feedback generation     |
| `POST` | `/evaluation/feedback/local`| AI feedback generation.    |

### 📤 **Request Format**

All analysis endpoints expect **multipart/form-data** with:

```http
Content-Type: multipart/form-data
Key: audio_file
Value: [Your audio file]
```

## ✨ Features

### 🔊 **Audio Analysis**

**Endpoint:** `evaluation/analyze_audio`

The audio analysis endpoint provides speech analysis information for a given audio file in `.wav`, `.mp3`, `.flac`, or `.m4a` format.

It leverages the project "My-Voice-Analysis" created by Shahabks, that can be found at the following [Github Repository](https://github.com/Shahabks/my-voice-analysis).

Using the [Praat Phonetic Model](http://www.praat.org/), it can return information on:

- **Speech rate:** Total number of syllables spoken per second (including pauses and fillers).
- **Articulation rate:** Total number of syllables spoken per second (excluding pauses and fillers).
- **Number of syllables:** Number of syllables spoken.
- **Count number of pauses:** Number of pauses and fillers.
- **Speaking time:** Speaking time (excluding fillers and pauses).
- **Total speaking time:** Speaking time (including fillers and pauses).
- **Speaking to Total Time Ratio:** Ratio between speaking duration and total speaking duration.

It also uses the [Whisper Speech Recognition Model](https://openai.com/index/whisper/) to create a transcription of the audio file.

#### 🗝️ Keys
- `audio_file` : Audio file in `.wav`, `.mp3`, `.flac`, or `.m4a` format.

#### 🧪 Testing
```bash
curl -X POST http://127.0.0.1:8000/evaluation/analyze_audio \
  -F "audio_file=@/full/path/to/your/file.wav"
```

#### Example output
```json
{
    "number_of_syllables": 10,
    "number_of_pauses": 0,
    "speech_rate": 3.0,
    "articulation_rate": 4.0,
    "speaking_duration": 2.6,
    "total_duration": 3.0,
    "ratio": 0.9,
    "transcription": "life is not an exact science it is an art"
}
```

### 🔊 **Audio Evaluation**

**Endpoint:** `evaluation/evaluate_audio`

The audio evaluation endpoint returns a graded evaluation between two audio files and their speech using the Speech Analysis information.

It contemplates the following evaluation points:

- **Clarity score:** Scored over 10 points, it considers the Word Error Rate of the two transcripts and the number of syllables. 
- **Speed Score:** Scored over 10 points, it considers the speech rate, speaking duration and total duration.
- **Articulation score:** Scored over 10 points, it considers the articulation rate and the number of syllables.
- **Rythm score:** Scored over 10 points, it considers speaking-to-total-time ratio and the number of pauses.
- **Total score:** Scored over 100% points, it is the sum of all the evaluation points scored over 100%.

#### 🗝️ Keys
- `user_analysis` : JSON analysis of user audio 
- `reference_analysis` : JSON analysis of reference audio

#### 🧪 Testing
```bash
curl -X POST http://localhost:8000/feedback \
  -F "reference_analysis={\"number_of_syllables\": 6, \"number_of_pauses\": 0, \"speech_rate\": 2.0, \"articulation_rate\": 2.0, \"speaking_duration\": 5.6, \"total_duration\": 6.0, \"ratio\": 0.9, \"transcription\": \"life is not an exact science it is an art\"}" \
  -F "user_analysis={\"number_of_syllables\": 13, \"number_of_pauses\": 0, \"speech_rate\": 3.0, \"articulation_rate\": 5.0, \"speaking_duration\": 2.7, \"total_duration\": 4.6, \"ratio\": 0.6, \"transcription\": \"life is not an exact science it is an art\"}"
```

#### Example output
```json
{
    "total_score": 88,
    "clarity_score": 10,
    "speed_score": 9,
    "articulation_score": 8,
    "rythm_score": 6
}
```

### 🤖 **AI-Powered Feedback**

**Endpoint:** `evaluation/feedback` and `evaluation/feedback/local`

The feedback endpoints provide AI generated feedback by using Large Language Models:

- **Non-local:** Qwen3-14B that can be found at [Arli AI](https://www.arliai.com/) 
that is hosted via a web server.
- **Local:** Mistral-7b that can be found at [Hugging Face](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF) that is hosted locally, using about 3-4 GB of RAM.

Both models will return feedback under the categories of:
- Speed
- Clarity
- Articulation
- Rythm

It will return three tips for each category with:
- One assesment of the speaker's performance compared to the reference.
- One tip on how to improve.
- One tip on how to improve in the future.

#### 🗝️ Keys
- `user_analysis` : JSON analysis of user audio 
- `reference_analysis` : JSON analysis of reference audio

#### 🧪 Testing
```bash
curl -X POST http://localhost:8000/feedback \
  -F "reference_analysis={\"number_of_syllables\": 6, \"number_of_pauses\": 0, \"speech_rate\": 2.0, \"articulation_rate\": 2.0, \"speaking_duration\": 5.6, \"total_duration\": 6.0, \"ratio\": 0.9, \"transcription\": \"life is not an exact science it is an art\"}" \
  -F "user_analysis={\"number_of_syllables\": 13, \"number_of_pauses\": 0, \"speech_rate\": 3.0, \"articulation_rate\": 5.0, \"speaking_duration\": 2.7, \"total_duration\": 4.6, \"ratio\": 0.6, \"transcription\": \"life is not an exact science it is an art\"}"
```

#### Example output
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

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8+
```

### Installation

#### 1. **Install dependencies**

```bash
    pip install typing
    pip install dotenv
    pip install os
    pip install fastapi
    pip install uvicorn
    pip install pydantic
    pip install requests
    pip install json
    pip install praat-parselmouth
    pip install numpy
    pip install scipy
    pip install jiwer
    pip install openai-whisper
    pip install llama_cpp_python
    pip install pydub
```

#### 2. **Download model file**

In order for the `evaluation/feedback/local` endpoint to work, the `.gguf` file containing the model must be downloaded from [Hugging Face](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF). 

Please download the file named `mistral-7b-instruct-v0.1.Q4_K_M.gguf` from the website and place it inside the directory named `models` found at `evaluation_api/core/feedback/models` with this exact name.

#### 3. **Configure the `.env` and `config.py` files**

Create a copy of the `.env.example` file with:

```bash
cp .env.example .env
```

Modify the `.env` file by replacing the variable `ARLI_API_KEY` with the API key 
that [Arli AI](https://www.arliai.com/) provides for **text generation models**.

#### 4. Modify ARLI API key parameters

Also please modify in the ARLI API key **parameters** option the following:
- Select the `Qwen3-14B-ArliAI-RpR-v5-Small` as the only **model**.
- If the Qwen model is not available, then please choose the `Gemma-3-27B-ArliAI-RPMax-v3` and the
`Gemma-3-27B-it` models in the **Multi Models** option.
- Mark the **hide thinking** checkbox to stop the model from sharing it's thought process.
- Click **save**.

The parameters that have been modified and applied will have a blue circle next to them.

Parameters using `Qwen3-14B-ArliAI-RpR-v5-Small`:
![Parameters Arli AI using Qwen](<parameters.png>)

Parameters using `Gemma-3-27B-ArliAI-RPMax-v3` and `Gemma-3-27B-it`:
![Parameters Arli AI using Gemma](<parameters2.png>)

More information on the different configurations that can be established can be found 
at the 
[Arli Text Generation API Documentation](https://www.arliai.com/docs?lang=en&_gl=1*5wid9d*_up*MQ..*_ga*MzY2ODIwNjcxLjE3NTM1NjQ3Nzk.*_ga_7X1GX4PZG5*czE3NTM1NjQ3NzgkbzEkZzEkdDE3NTM1NjQ3OTEkajQ3JGwwJGgw). 

### 5. **Run the API**

In order to run the API, in terminal make sure you are located in the `evaluation_api/app` folder with:
```bash
cd API/evaluation_api/app
```
Once this is done, just run:
```bash
python3 main.py
```
Or: 
```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:xxxx`

## 🏗️ Architecture

### 📁 **Project Structure**

``` bash
evaluation_api/
├── core/                           # Logic handling
│   ├── analysis/              
|   |   ├── analyzer.py             # Speech analysis
|   |   └── myspsolution.praat      # Configuration file for PRAAT
│   ├── evaluation/            
|   |   └── evaluator.py            # Audio grading system 
|   ├── feedback/   
|   |   ├── models/  
|   |   |   └── mistral-7b-instruct-v0.1.Q4_K_M.gguf  # Model file      
|   |   ├── advisor.py              # Web hosted AI feedback
|   |   └── local_advisor.py        # Locally hosted AI feedback
|   ├── transcription/ 
|   |   └── transcriber.py          # Audio transcriptions 
|   └── utils/ 
|       └── audio_tools.py          # Normalize wav audio file
├── app/
│   └── main.py                     # FastAPI application
├── routers/
│   └── evaluation_router.py        # API endpoints
├── services/
│   ├── analysis_service.py         # Speech analysis
│   ├── evaluation_service.py       # Speech grading
│   ├── feedback_service.py         # Web AI feedback generation
│   └── local_feeback_service.py    # Local AI feedback generation
├── schemas/
│   └── evaluation_schema.py        # Pydantic models
├── .env                            # API Configuration file
└── config.py                       # Configuration file
```

## 🙏 Acknowledgments

- **[Parselmouth](https://github.com/YannickJadoul/Parselmouth)**: Python interface to Praat
- **[Praat](http://www.praat.org/)**: Phonetic analysis software
- **[Whisper](https://openai.com/index/whisper/)**: Automatic Speech Recognition Model
- **[My-Voice-Analysis](https://github.com/Shahabks/my-voice-analysis)**: Python library for the analysis of voice 
- **[Arli AI](https://www.arliai.com/)**: AI Inference API Platform
- **[Mistral-7B-Instruct](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)**: TheBloke's LLM 
---
