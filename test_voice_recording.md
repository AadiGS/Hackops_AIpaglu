# Voice Recording Test Guide

## Quick Setup & Test

### 1. Start Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
**Expected Output:**
```
Loading emotion detection model...
Model loaded successfully.
Starting Emotion Detection API...
Server will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs
```

### 2. Start Frontend
```bash
cd frontend1
npm install
npm run dev
```
**Expected Output:**
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
```

### 3. Test the Voice Recording Feature

1. **Open Browser**: Go to `http://localhost:3000/dashboard`
2. **Test Backend Connection**: Click the "Test Backend" button
   - Should show: "Backend is running! Status: healthy, Model loaded: true"
3. **Start Recording**: Click "Start Recording" button
   - Should show recording timer and "Stop Recording" button
4. **Speak**: Say something like "I'm feeling really happy today"
5. **Stop Recording**: Click "Stop Recording" button
6. **Wait for Analysis**: You'll see "Analyzing Your Voice..." indicator
7. **View Results**: Should show transcription, mood, and song recommendations

## Troubleshooting

### If "Test Backend" fails:
- Make sure backend is running on port 8000
- Check if all dependencies are installed
- Look at backend console for errors

### If recording doesn't work:
- Check browser microphone permissions
- Open browser console (F12) for error messages
- Try refreshing the page

### If analysis fails:
- Check backend console for API errors
- Verify API keys in `.env` file
- Check network tab in browser dev tools

## Expected Flow:
1. ✅ Click "Start Recording" → Timer starts, red stop button appears
2. ✅ Speak for 3-10 seconds → Audio is recorded
3. ✅ Click "Stop Recording" → Processing indicator shows
4. ✅ Wait 10-30 seconds → Results appear with transcription and songs

## Debug Information:
- Check browser console (F12) for detailed logs
- Check backend terminal for API call logs
- Audio file size should be > 0 bytes in console logs
