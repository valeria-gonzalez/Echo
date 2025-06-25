# 🎯 Pronunciation Evaluation API

## 📋 Overview

A comprehensive **FastAPI-based microservice** that analyzes English
pronunciation using **Praat acoustic analysis** and
**AI-powered feedback generation**. This API provides detailed voice
quality metrics, personalized recommendations, and practice tips for English
language learners.

## ✨ Features

### 🔊 **Audio Analysis**

- **Pitch Analysis**: Mean frequency, stability (jitter)
- **Volume Control**: Intensity measurement, stability (shimmer)
- **Formant Detection**: F1/F2 frequencies for vowel quality
- **Duration Tracking**: Speech timing analysis

### 🤖 **AI-Powered Feedback**

- **Smart Scoring**: 0-10 pronunciation quality score
- **Detailed Analysis**: Professional voice coaching feedback
- **Personalized Tips**: Custom practice recommendations

### 📊 **Supported Formats**

- Audio files: `.wav`, `.mp3`, `.flac`, `.ogg`
- Real-time processing with temporary file handling
- Comprehensive error handling and validation

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8+
pip install -r requirements.txt
```

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd Echo/evaluation_api
```

2. **Install dependencies**

```bash
pip install -r ../requirements.txt
```

3. **Install Praat** (Required for audio analysis)

- **Windows**: Download from [Praat.org](http://www.praat.org/)
- **macOS**: `brew install praat`
- **Linux**: `sudo apt-get install praat`

4. **Run the API**

```bash
cd app
python main.py
```

The API will be available at: `http://localhost:xxxx`

## 📚 API Documentation

### 🔗 **Endpoints**

| Method | Endpoint                    | Description                |
| ------ | --------------------------- | -------------------------- |
| `GET`  | `/`                         | Welcome message            |
| `POST` | `/evaluation/analyze_audio` | Raw Praat analysis         |
| `POST` | `/evaluation/feedback`      | AI feedback generation     |
| `POST` | `/evaluation/tips`          | Personalized practice tips |

### 📤 **Request Format**

All analysis endpoints expect **multipart/form-data** with:

```http
Content-Type: multipart/form-data

Key: audio_file
Value: [Your audio file]
```

### 📥 **Response Examples**

#### **Audio Analysis** (`/analyze_audio`)

```json
{
  "pitch_mean_hz": 145.67,
  "intensity_mean_db": 68.45,
  "jitter_local_percent": 0.82,
  "shimmer_local_db": 0.67,
  "f1_mid_hz": 520.33,
  "f2_mid_hz": 1480.21,
  "duration_s": 3.245,
  "message": "Audio analysis completed successfully."
}
```

#### **AI Feedback** (`/feedback`)

```json
{
  "overall_score": 7.5,
  "detailed_feedback": "Your pronunciation shows good volume control and natural pitch range. Consider working on pitch stability for smoother delivery.",
  "vocal_characteristics": {
    "pitch": "Normal pitch range, very natural",
    "intensity": "Good volume range, clear and natural",
    "jitter": "Good pitch stability, within normal range",
    "shimmer": "Good volume stability, smooth delivery"
  },
  "recommendations": [
    "Practice sustained vowel sounds to improve pitch stability",
    "Work on breath support for steadier voice production",
    "Focus on consistent airflow during speech"
  ],
  "praat_data": {
    /* Raw analysis data */
  }
}
```

#### **Practice Tips** (`/tips`)

```json
{
  "personalized_tips": [
    "Practice humming English melodies to improve pitch control",
    "Breathe from your diaphragm, not your chest",
    "Record yourself daily and compare with native speakers"
  ],
  "exercises": [
    "Sustain 'ahh' sound for 15 seconds with steady pitch",
    "Count from 1 to 20 maintaining consistent volume",
    "Practice tongue twisters focusing on clear articulation"
  ],
  "focus_areas": ["Pitch stability", "Volume control"],
  "difficulty_level": "Intermediate - Skill building",
  "praat_data": {
    /* Raw analysis data */
  }
}
```

## 🏗️ Architecture

### 📁 **Project Structure**

```
evaluation_api/
├── app/
│   └── main.py              # FastAPI application
├── routers/
│   └── evaluation_router.py # API endpoints
├── services/
│   ├── praat_service.py     # Acoustic analysis
│   └── feedback_service.py  # AI feedback generation
├── schemas/
│   └── evaluation_schema.py # Pydantic models
└── models/
    └── evaluation_model.py  # (Future: Database models)
```

### 🔧 **Core Components**

#### **PraatService**

- Handles audio file processing
- Performs acoustic analysis using Parselmouth
- Extracts voice quality metrics
- Manages temporary file operations

#### **FeedbackService**

- Uses Google Flan-T5 model for AI feedback
- Generates personalized recommendations
- Calculates pronunciation scores
- Creates practice exercises

#### **Evaluation Router**

- RESTful API endpoints
- File validation and error handling
- Response formatting and serialization

## 🔬 Technical Details

### **Voice Analysis Metrics**

| Metric             | Description           | Normal Range |
| ------------------ | --------------------- | ------------ |
| **Pitch (Hz)**     | Fundamental frequency | 85-250 Hz    |
| **Intensity (dB)** | Volume level          | 55-75 dB     |
| **Jitter (%)**     | Pitch stability       | < 1.04%      |
| **Shimmer (dB)**   | Volume stability      | < 1.0 dB     |
| **F1/F2 (Hz)**     | Vowel formants        | Variable     |

### **AI Model Integration**

- **Model**: Google Flan-T5 (Text-to-Text Transfer Transformer)
- **Use Case**: Pronunciation feedback generation
- **Input**: Voice analysis metrics + context
- **Output**: Structured feedback and recommendations

### **Scoring Algorithm**

```python
# Base score: 10.0
score = 10.0

# Deduct points for:
- Jitter > 1.04%: -1.5 to -3.0 points
- Shimmer > 1.0 dB: -1.2 to -2.5 points
- Intensity < 55 or > 85 dB: -1.0 to -2.0 points
- Pitch < 70 or > 300 Hz: -0.5 to -1.5 points

# Final score: 0.0 - 10.0
```

## 🔧 Configuration

### **Environment Variables**

```bash
# Optional: Model configuration
MODEL_NAME=google/flan-t5-base  # Use smaller model for development
HUGGINGFACE_CACHE_DIR=/path/to/cache

# Optional: API configuration
HOST=0.0.0.0
PORT=5000
DEBUG=true
```

### **Model Selection**

```python
# Development (faster, less accurate)
self.model_name = "google/flan-t5-base"

# Production (slower, more accurate)
self.model_name = "google/flan-t5-large"
```

## 🧪 Testing

### **Manual Testing with cURL**

```bash
# Test audio analysis
curl -X POST "http://localhost:5000/evaluation/analyze_audio" \
  -H "Content-Type: multipart/form-data" \
  -F "audio_file=@your_audio.wav"

# Test AI feedback
curl -X POST "http://localhost:5000/evaluation/feedback" \
  -H "Content-Type: multipart/form-data" \
  -F "audio_file=@your_audio.wav"
```

### **Using Postman**

1. Set method to `POST`
2. URL: `http://localhost:5000/evaluation/feedback`
3. Body → form-data
4. Key: `audio_file` (File type)
5. Value: Select your audio file

## 🚨 Error Handling

### **Common Error Responses**

```json
// Invalid file type
{
  "detail": "Invalid file type. Please upload an audio file."
}

// Praat analysis failed
{
  "detail": "Praat analysis failed: [specific error]"
}

// Empty audio file
{
  "detail": "Audio file is empty."
}
```

## 🙏 Acknowledgments

- **[Parselmouth](https://github.com/YannickJadoul/Parselmouth)**: Python interface to Praat
- **[Hugging Face Transformers](https://huggingface.co/transformers/)**: AI model integration
- **[FastAPI](https://fastapi.tiangolo.com/)**: Modern API framework
- **[Praat](http://www.praat.org/)**: Phonetic analysis software

---
