# EchoMind - AI Mock Interview Coach

Records a spoken answer to a behavioral interview question, transcribes it with
OpenAI's Whisper speech recognition model, then analyzes the delivery: filler
word frequency, speaking pace, hedging language, and an overall confidence score.

Tech Stack: Python, OpenAI Whisper, Flask, React.js, MediaRecorder API

## Features
- In-browser audio recording using the native MediaRecorder API, no plugins required
- Speech-to-text transcription using Whisper (runs locally, no API key needed)
- Filler word detection (um, uh, like, you know, and more)
- Speaking pace calculation in words per minute
- Hedging language detection (I think, maybe, I guess) that can undercut perceived confidence
- Plain-language feedback generated from the combined signals, similar to what a human coach would say

## How It Works
1. The React frontend records the candidate's spoken answer and uploads it as a webm audio blob
2. The Flask backend runs the audio through Whisper's "base" model to get a transcript
3. `utils/analyzer.py` scans the transcript for filler words and hedging phrases using
 word-boundary regex matching, and computes speaking pace from word count and audio duration
4. A confidence score is derived by penalizing high filler rate, excessive hedging, and answers that are too short


## Getting Started

### Backend
```
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# Whisper requires ffmpeg installed on your system (see requirements.txt comment)
python app.py
```
Server runs on http://localhost:5000

### Frontend
```
cd frontend
npm install
npm run dev
```
App runs on http://localhost:5173 (browser will ask for microphone permission)

## API
| Method | Endpoint | Description |
|--------|-------------------------|--------------------------------------------------------------|
| GET | /api/questions | List of practice interview questions |
| POST | /api/evaluate-answer | multipart form: audio file -- returns transcript + delivery analysis |

## Roadmap
- Facial expression analysis during recording for combined verbal + nonverbal feedback
- Question-specific answer quality scoring using the STAR method structure
- Session history so a candidate can track improvement over time

---
Built by Anusha V - https://www.linkedin.com/in/anushav20
