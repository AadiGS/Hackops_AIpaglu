import os
import requests
import time
import json
from pathlib import Path
import sys
import sounddevice as sd
import wavio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY", "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")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDZOmGfvq3sqftTmvQzTIaLGmDM-HzA5JA")

BASE_URL = "https://api-inference.huggingface.co/models/"
WHISPER_MODEL = "openai/whisper-large-v3"
EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

sys.stdout.reconfigure(encoding='utf-8')

# ------------------- Audio Recording -------------------
def record_live_audio(filename="live_audio.wav", duration=10, fs=44100):
    print(f"\n🎙️ Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wavio.write(filename, recording, fs, sampwidth=2)
    print(f"✅ Saved recording to {filename}")
    return filename

# ------------------- Transcription -------------------
def transcribe_audio(audio_path):
    url = BASE_URL + WHISPER_MODEL
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    headers = HEADERS.copy()
    headers["Content-Type"] = "audio/wav"
    resp = requests.post(url, headers=headers, data=audio_bytes, timeout=120)
    if resp.status_code == 200:
        text = resp.json().get("text", "").strip()
        return text if text else None
    return None

# ------------------- Emotion Detection -------------------
def analyze_emotion(text):
    url = BASE_URL + EMOTION_MODEL
    payload = {"inputs": text}
    resp = requests.post(url, headers=HEADERS, json=payload, timeout=60)
    if resp.status_code == 200:
        emotions = resp.json()[0]
        emotions.sort(key=lambda x: x['score'], reverse=True)
        top = emotions[0]
        return top['label'], top['score'], emotions
    return None, 0, []

# ------------------- Gemini API for Songs -------------------
def get_gemini_mood_info(mood):
    if not GEMINI_API_KEY:
        return {"desc": "No Gemini API key found.", "songs": []}
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-native-audio-preview-09-2025:generateContent"
    prompt = (
        f"Give a 1-line Hindi description of the mood '{mood}' and "
        f"list top 5 popular Indian songs (any language) matching this mood.\n"
        f"Format: description first, then numbered list."
    )
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 256}
    }
    try:
        resp = requests.post(url, params={"key": GEMINI_API_KEY}, json=data, timeout=30)
        if resp.status_code == 200:
            text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            desc = lines[0]
            songs = [l for l in lines[1:6]]  # take top 5 songs
            return {"desc": desc, "songs": songs}
        else:
            return {"desc": f"Gemini API error: {resp.text}", "songs": []}
    except Exception as e:
        return {"desc": str(e), "songs": []}

# ------------------- Pipeline -------------------
def speech_to_mood_pipeline(duration=10):
    audio_file = record_live_audio(duration=duration)
    text = transcribe_audio(audio_file)
    if not text:
        print("❌ Could not transcribe audio.")
        return
    mood, confidence, all_emotions = analyze_emotion(text)
    print(f"\n📝 Transcription: {text}")
    print(f"🎯 Detected mood: {mood} (confidence: {confidence:.2f})")
    
    gemini_info = get_gemini_mood_info(mood)
    print(f"\n🔎 Mood description (Hindi): {gemini_info['desc']}")
    print("🎶 Top 5 Indian songs for this mood:")
    for song in gemini_info["songs"]:
        print(f"  ♪ {song}")

    result = {
        "file": audio_file,
        "transcription": text,
        "primary_mood": mood,
        "confidence": confidence,
        "all_emotions": all_emotions,
        "gemini": gemini_info
    }
    out_file = f"mood_analysis_{int(time.time())}.json"
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Results saved to {out_file}")

# ------------------- Main -------------------
if __name__ == "__main__":
    duration = int(input("⏱️ Enter recording duration (seconds): "))
    speech_to_mood_pipeline(duration)
