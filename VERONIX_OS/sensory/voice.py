import asyncio
import threading
import queue
import tempfile
import os
import time
import edge_tts
from playsound import playsound
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TTS")

class TTSEngine:
    def __init__(self):
        print("[TTS] Initializing Edge TTS (Natural Voice)...")

        self.q = queue.Queue()
        self.voice = "en-US-AriaNeural"  # High-quality neural voice
        self.rate = "+0%"
        self.volume = "+0%"
        self.shutdown_event = threading.Event()

        #  Background worker starts immediately
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

        print("[TTS] READY ")

    
    # ASYNC EDGE TTS GENERATOR
    
    async def _speak_async(self, text, file_path):
        """Generate speech with specialized network settings"""
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=self.rate,
            volume=self.volume
        )
        # communicate.save handles the connection to Bing servers
        await communicate.save(file_path)

    # ----------------------------
    # BACKGROUND WORKER (The Engine Room)
    # ----------------------------
    def _worker(self):
        """Background worker thread with persistent retry logic for timeouts"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        while not self.shutdown_event.is_set():
            try:
                # Wait for text from the bridge/main OS
                text = self.q.get(timeout=1)
            except queue.Empty:
                continue

            success = False
            max_retries = 3
            
            # --- CONNECTION RETRY LOOP ---
            for attempt in range(max_retries):
                file_path = None
                try:
                    # 1. Create a safe temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                        file_path = f.name
                    
                    # 2. Attempt to generate audio from Edge servers
                    # We wrap this in a timeout/retry because GPU load can delay handshakes
                    loop.run_until_complete(self._speak_async(text, file_path))
                    
                    # 3. Play audio
                    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                        playsound(file_path)
                        success = True
                        break # Exit retry loop on success
                    
                except Exception as e:
                    logger.warning(f"[TTS] Connection Attempt {attempt + 1} failed. Retrying...")
                    time.sleep(1) # Small buffer for network to stabilize
                
                finally:
                    # 4. Clean up temp file immediately after play or failure
                    if file_path and os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            logger.warning(f"Cleanup failed for {file_path}: {e}")

            if not success:
                logger.error(f" TTS FAILURE: Could not connect to Edge servers after {max_retries} tries.")

    # ----------------------------
    # PUBLIC INTERFACE
    # ----------------------------
    def speak(self, text: str):
        """Queue text for speech synthesis (non-blocking)"""
        if not text:
            return

        # Push text to the queue and let the worker handle the timing
        self.q.put(text)
        logger.debug(f"Queued speech: {text[:30]}...")
    
    # ----------------------------
    # SHUTDOWN PROTOCOL
    # ----------------------------
    def shutdown(self):
        """Gracefully shutdown TTS engine and cleanup worker"""
        print("[TTS] Shutting down Voice Core...")
        self.shutdown_event.set()
        if self.worker_thread.is_alive():
            self.worker_thread.join(timeout=2)