import os
import wave
import numpy as np
import winsound
import sounddevice as sd
from faster_whisper import WhisperModel
from piper.voice import PiperVoice

# --- PATHS ---
MODEL_ONNX = r"D:\AGI_Universal_Project\Models\en_US-lessac-medium.onnx"
WAV_PATH = r"D:\AGI_Universal_Project\sensor_test.wav"

print("--- F.R.I.D.A.Y. SENSOR CHECK ---")

# 1. TEST TTS (Speaking)
print("[1/2] Testing TTS (Piper)...")
try:
    voice = PiperVoice.load(MODEL_ONNX)
    test_text = "Systems check. Audio output functional. Can you hear me, Boss?"
    with wave.open(WAV_PATH, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(22050)
        voice.synthesize(test_text, wav_file)
    winsound.PlaySound(WAV_PATH, winsound.SND_FILENAME)
    print(">> TTS SUCCESS")
except Exception as e:
    print(f">> TTS FAILED: {e}")

# 2. TEST STT (Listening)
print("\n[2/2] Testing STT (Whisper)...")
print("Say something clearly into the mic now (4 seconds)...")
try:
    stt_engine = WhisperModel("small.en", device="cpu", compute_type="int8")
    audio = sd.rec(int(4 * 16000), samplerate=16000, channels=1, dtype='float32')
    sd.wait()
    audio_data = np.squeeze(audio)
    
    segments, _ = stt_engine.transcribe(audio_data, vad_filter=True)
    user_input = " ".join([s.text for s in segments]).strip()
    
    if user_input:
        print(f">> STT SUCCESS. I heard: '{user_input}'")
    else:
        print(">> STT FAILED: No speech detected. Check your mic settings.")
except Exception as e:
    print(f">> STT FAILED: {e}")

print("\n--- CHECK COMPLETE ---")