# sensory/listen.py

import sounddevice as sd
import numpy as np
import time
import threading

class STTEngine:
    def __init__(self):
        print("[DEBUG_STT]  INIT: Creating NEW STTEngine instance (ID: {})".format(id(self)))
        
        self.model_ready = False
        self.audio_buffer = []
        self.samplerate = 16000
        
        # Fixed Parameters to handle background hum
        self.SILENCE_THRESHOLD = 0.010  
        # Increased from 0.015 to 0.025 to ignore tiny environmental vibrations (0.019)
        self.SPEECH_THRESHOLD = 0.025   
        self.MIN_SILENCE_DURATION = 0.5 
        
        self.can_process_audio = threading.Event()
        
        try:
            print("[DEBUG_STT]   Setting up Microphone Stream...")
            self.stream = sd.InputStream(
                samplerate=self.samplerate, 
                channels=1, 
                callback=self._audio_callback,
                device=1
            )
            self.stream.start()
            
            print("[DEBUG_STT] 🎧 Stream Created. Loading Heavy Whisper Model (GPU)...")
            
            # SIMULATED SLOW LOADING (Replace with Real Model Load)
            # If you have the real whisper model, load it here instead of sleeping
            # e.g., self.model = whisper.load_model("base")
            time.sleep(10.0)
            
            print("[DEBUG_STT]  Whisper Model Loaded. Releasing Audio Gate.")
            self.model_ready = True
            self.can_process_audio.set()
            
        except Exception as e:
            print(f"[DEBUG_STT]  Stream FAILED to start: {e}")
            raise e

    def _audio_callback(self, indata, frames, time_info, status):
        if not self.can_process_audio.is_set():
            return 
        try:
            self.audio_buffer.append(indata.copy())
        except Exception:
            pass

    def listen(self):
        print("[DEBUG_STT]   ENTERING listen(). Waiting for Activation...")
        self.can_process_audio.wait()
        self.audio_buffer = []
        
        speech_frames = []
        silence_chunks = 0
        silence_limit = int(self.MIN_SILENCE_DURATION * 100)
        
        # PHASE 1: Wait for Trigger (User must speak)
        print("[DEBUG_STT]  Phase 1: Waiting for speech trigger...")
        timeout_counter = 0
        while True:
            if len(self.audio_buffer) > 0:
                data = self.audio_buffer.pop(0)
                volume = np.linalg.norm(data) * 10
                
                if volume > self.SPEECH_THRESHOLD:
                    print(f"[DEBUG_STT] 🎤 Speech Detected! ({volume:.3f})")
                    speech_frames.append(data)
                    break
            else:
                time.sleep(0.01)
                
            timeout_counter += 1
            if timeout_counter > 1000: 
                print("[DEBUG_STT]   Global Timeout (10s). No speech detected.")
                return "" # STRICT RETURN. No hallucinations.

       # sensory/listen.py

import sounddevice as sd
import numpy as np
import time
import threading

class STTEngine:
    def __init__(self):
        print("[DEBUG_STT]  INIT: Creating NEW STTEngine instance (ID: {})".format(id(self)))
        
        self.model_ready = False
        self.audio_buffer = []
        self.samplerate = 16000
        
        # Fixed Parameters to handle background hum
        self.SILENCE_THRESHOLD = 0.010  
        # Increased from 0.015 to 0.025 to ignore tiny environmental vibrations (0.019)
        self.SPEECH_THRESHOLD = 0.025   
        self.MIN_SILENCE_DURATION = 0.5 
        
        self.can_process_audio = threading.Event()
        
        try:
            print("[DEBUG_STT]   Setting up Microphone Stream...")
            self.stream = sd.InputStream(
                samplerate=self.samplerate, 
                channels=1, 
                callback=self._audio_callback,
                device=1
            )
            self.stream.start()
            
            print("[DEBUG_STT]  Stream Created. Loading Heavy Whisper Model (GPU)...")
            
            # --- SIMULATED SLOW LOADING ---
            # Keep this for now so the UI doesn't hang while testing.
            # Once ready, remove this and uncomment the 'Real Model Load' section below.
            time.sleep(10.0)
            
            print("[DEBUG_STT]  Whisper Model Loaded. Releasing Audio Gate.")
            self.model_ready = True
            self.can_process_audio.set()
            
        except Exception as e:
            print(f"[DEBUG_STT]  Stream FAILED to start: {e}")
            raise e

    def _audio_callback(self, indata, frames, time_info, status):
        """Callback for the microphone stream."""
        if not self.can_process_audio.is_set():
            return 
        try:
            # Append a copy of the data to our buffer
            self.audio_buffer.append(indata.copy())
        except Exception:
            # Ignore buffer overflow errors for now
            pass

    def listen(self):
        """
        Main listening logic.
        Waits for speech, records it, and returns transcribed text.
        Returns empty string "" if nothing valid is said.
        """
        print("[DEBUG_STT]   ENTERING listen(). Waiting for Activation...")
        
        # Wait for model to be ready
        self.can_process_audio.wait()
        
        # Clear buffer to start fresh
        self.audio_buffer = []
        
        speech_frames = []
        silence_chunks = 0
        silence_limit = int(self.MIN_SILENCE_DURATION * 100)
        
        # --- PHASE 1: Wait for Trigger ---
        print("[DEBUG_STT]  Phase 1: Waiting for speech trigger...")
        timeout_counter = 0
        while True:
            if len(self.audio_buffer) > 0:
                data = self.audio_buffer.pop(0)
                # Calculate volume (RMS amplitude)
                volume = np.linalg.norm(data) * 10
                
                if volume > self.SPEECH_THRESHOLD:
                    print(f"[DEBUG_STT] 🎤 Speech Detected! ({volume:.3f})")
                    speech_frames.append(data)
                    break
            else:
                time.sleep(0.01)
                
            timeout_counter += 1
            # Hard timeout: If user doesn't speak in 10 seconds, exit.
            if timeout_counter > 1000: 
                print("[DEBUG_STT]   Global Timeout (10s). No speech detected.")
                return "" 

        # --- PHASE 2: Record until Silence ---
        print("[DEBUG_STT]  Phase 2: Recording...")
        while True:
            if len(self.audio_buffer) > 0:
                data = self.audio_buffer.pop(0)
                volume = np.linalg.norm(data) * 10
                speech_frames.append(data)
                
                # Check if current chunk is silent
                if volume < self.SILENCE_THRESHOLD:
                    silence_chunks += 1
                else:
                    silence_chunks = 0
            else:
                time.sleep(0.01)
                silence_chunks += 1
            
            # Stop recording if silence is long enough
            if silence_chunks > silence_limit:
                print(f"[DEBUG_STT]  Silence Detected. Stopping.")
                break
                
            # Stop recording if max length (30 seconds) is reached
            if len(speech_frames) > (30 * self.samplerate / 100):
                print("[DEBUG_STT]   Max length reached.")
                break

        print(f"[DEBUG_STT]   EXITING listen(). Processed {len(speech_frames)} frames.")
        
        # --- VALIDATION ---
        # If audio is too short (< 50 frames), ignore it (likely a click or pop).
        if len(speech_frames) < 50: 
            print("[DEBUG_STT]  Audio too short. Ignoring.")
            return ""
            
        # Combine all recorded chunks into one array
        audio_np = np.concatenate(speech_frames, axis=0).flatten()
        
        # --- REAL WHISPER PROCESSING ---
        # This is where the magic happens.
        # Uncomment the block below when you want to use the real model.
        
        # try:
        #     # self.model should be loaded in __init__ if you remove the sleep(10.0)
        #     result = self.model.transcribe(audio_np, language="en") 
        #     text = result["text"].strip()
        #     print(f"[DEBUG_STT]  Whisper Success: '{text}'")
        #     return text
        # except Exception as e:
        #     print(f"[DEBUG_STT]  Whisper Error: {e}")
        #     return ""

        # --- CURRENT STATE (SIMULATION OFF) ---
        # Since the real model is not loaded yet (we used time.sleep(10.0)),
        # we return EMPTY. This ensures the system stays quiet unless real input is processed.
        return ""