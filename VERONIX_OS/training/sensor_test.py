import os
import speech_recognition as sr
import pyttsx3
import whisper
import numpy as np

def test_sensors():
    # 1. Initialize Voice
    print("--- 🔊 INITIALIZING SOVEREIGN VOICE ---")
    engine = pyttsx3.init()
    engine.say("Sensor calibration active. Testing hardware arrays.")
    engine.runAndWait()

    # 2. Load Local Brain (Whisper)
    print("--- 🧠 LOADING WHISPER (TINY MODEL) ---")
    model = whisper.load_model("tiny")

    # 3. Test Hearing
    # Change this to 1, then 9, if 5 remains silent
    MIC_ID = 1 
    r = sr.Recognizer()
    
    # --- SENSITIVITY CALIBRATION ---
    r.energy_threshold = 150  # Very sensitive to catch distant or quiet speech
    r.dynamic_energy_threshold = False # Fixed threshold for hardware testing
    
    print(f"\n--- 🔬 PROBING MIC ID {MIC_ID} ---")
    try:
        with sr.Microphone(device_index=MIC_ID) as source:
            print("Cleaning noise... (Stay silent)")
            # Shorter duration so we don't accidentally filter your voice out
            r.adjust_for_ambient_noise(source, duration=1) 
            
            print(">>> [LISTENING] SAY: 'Veronix, are you online?'")
            audio = r.listen(source, timeout=10, phrase_time_limit=5)
            
            # --- DATA VISUALIZER ---
            byte_count = len(audio.get_raw_data())
            print(f"Signal Strength: {byte_count} bytes captured.")
            
            if byte_count < 1000:
                print("⚠️ Warning: Data stream is too thin. Mic might be muted or wrong ID.")

            print("Signal captured. Processing Raw Array (FFmpeg Bypass)...")
            
            # Convert raw bytes directly to a float32 array
            raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
            audio_array = np.frombuffer(raw_data, np.int16).flatten().astype(np.float32) / 32768.0
            
            # Feed the array directly to the model
            result = model.transcribe(audio_array, fp16=False)
            text = result["text"].strip()
            
            if text:
                print(f"\n✅ SUCCESS! VERONIX HEARD: '{text}'")
                engine.say(f"I heard you say: {text}")
                engine.runAndWait()
            else:
                print("\n⚠️ Signal processed but no speech recognized. Check Windows Mic Gain or move closer.")

    except Exception as e:
        print(f"❌ SENSOR ERROR: {e}")
        print("\nACTION: If this timed out, change MIC_ID to 5 or 9 in the code.")

if __name__ == "__main__":
    test_sensors()