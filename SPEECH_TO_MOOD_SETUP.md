# Speech-to-Mood Integration Setup Guide

## Overview
This guide explains how to set up and use the speech-to-mood analysis feature that has been integrated into your MoodTune AI application.

## Features Added

### Backend (FastAPI)
- **New Dependencies**: Added `requests`, `sounddevice`, `wavio`, and `python-dotenv`
- **Environment Variables**: Created `.env` file with Hugging Face and Gemini API keys
- **New Endpoints**:
  - `POST /speech-to-mood` - Records audio and analyzes mood
  - `POST /upload-audio-mood` - Uploads audio file for mood analysis
- **Speech-to-Mood Pipeline**:
  1. Audio recording/upload
  2. Speech transcription using Hugging Face Whisper
  3. Emotion analysis using DistilRoBERTa
  4. Song recommendations using Gemini AI

### Frontend (Next.js)
- **Voice Recording**: Added microphone access and recording functionality
- **Real-time UI**: Shows recording status and processing indicators
- **Results Display**: Beautiful card layout showing:
  - Transcription of spoken text
  - Detected mood with confidence score
  - Hindi mood description
  - Top 5 recommended Indian songs

## Setup Instructions

### 1. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
cd backend
python main.py
```
The server will start at `http://localhost:8000`

### 3. Start the Frontend
```bash
cd frontend1
npm install
npm run dev
```
The frontend will start at `http://localhost:3000`

### 4. Test the Integration
```bash
cd backend
python test_speech_to_mood.py
```

## How to Use

### Voice Recording
1. Open the dashboard at `http://localhost:3000`
2. Click the "Record Voice" button
3. Allow microphone access when prompted
4. Speak for up to 10 seconds (recording stops automatically)
5. Wait for the AI analysis to complete
6. View your results including transcription, mood, and song recommendations

### API Endpoints

#### Record and Analyze Voice
```bash
curl -X POST "http://localhost:8000/speech-to-mood" \
  -H "Content-Type: application/json" \
  -d '{"duration": 10}'
```

#### Upload Audio File
```bash
curl -X POST "http://localhost:8000/upload-audio-mood" \
  -F "file=@your_audio_file.wav"
```

## API Response Format
```json
{
  "transcription": "I'm feeling really happy today",
  "primary_mood": "joy",
  "confidence": 0.95,
  "all_emotions": [
    {"label": "joy", "score": 0.95},
    {"label": "love", "score": 0.03},
    {"label": "anger", "score": 0.02}
  ],
  "mood_description": "खुशी से भरपूर मूड - आप बहुत खुश लग रहे हैं",
  "recommended_songs": [
    "1. Chaiyya Chaiyya - Dil Se",
    "2. Aaj Ki Raat - Don",
    "3. Tum Hi Ho - Aashiqui 2",
    "4. Kabira - Yeh Jawaani Hai Deewani",
    "5. Gerua - Dilwale"
  ]
}
```

## Troubleshooting

### Common Issues

1. **Microphone Access Denied**
   - Ensure browser has microphone permissions
   - Check browser settings for localhost

2. **Backend Connection Failed**
   - Verify backend is running on port 8000
   - Check if all dependencies are installed

3. **API Key Issues**
   - Verify `.env` file exists in backend directory
   - Check if API keys are valid

4. **Audio Recording Issues**
   - Ensure microphone is connected and working
   - Check browser console for errors

### Dependencies Issues
If you encounter import errors:
```bash
# Install missing packages
pip install sounddevice wavio python-dotenv requests

# For Windows users, you might need:
pip install portaudio  # for sounddevice
```

## File Structure
```
backend/
├── main.py                 # Updated with speech-to-mood endpoints
├── requirements.txt        # Updated with new dependencies
├── .env                   # API keys configuration
└── test_speech_to_mood.py # Test script

frontend1/
└── app/dashboard/page.tsx  # Updated with voice recording UI
```

## Next Steps
- Customize the recording duration
- Add more emotion models
- Implement playlist creation from recommendations
- Add voice command features
- Enhance the UI with animations

## Support
If you encounter any issues, check the browser console and backend logs for detailed error messages.
