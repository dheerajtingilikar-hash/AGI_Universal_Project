import os
# CRITICAL: Resolve OpenMP conflict between PyQt5 and AI backends
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# Limit threads to keep the GUI responsive
os.environ["OMP_NUM_THREADS"] = "1"

import sys
import time
import threading
import queue
import signal
from dataclasses import dataclass

import httpx
import asyncio
from ollama import Client

# =========================
# WINDOWS & PATH FIX
# =========================
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSplitter, QTextEdit
from PyQt5.QtCore import Qt, QObject, pyqtSlot, pyqtSignal

# Import custom modules
from interface.Theme import get_stylesheet
from interface.Neural_monitor import NeuralMonitorPanel
from interface.Subsystem_panel import SubsystemPanel
from interface.Screener_panel import ScreenerPanel
from interface.Keyboard_widget import KeyboardWidget

shutdown_event = threading.Event()
speaking_event = threading.Event()
# Global lock to ensure STT doesn't spin up until everything is settled
system_settled = threading.Event()

# =========================
# CONFIG & MODEL MANAGER
# =========================
@dataclass
class Config:
    OLLAMA_URL: str = "http://127.0.0.1:11434"
    MODEL: str = "llama3.2:3b"
    # Added path for the massive manifesto
    MANIFESTO_PATH: str = os.path.join(BASE_DIR, "config", "unbiased_core.txt")

config = Config()

class ModelManager:
    def __init__(self):
        self.client = None
        self.system_instruction = ""

    def init(self):
        # 1. Load the 2000-line Manifesto
        try:
            if os.path.exists(config.MANIFESTO_PATH):
                with open(config.MANIFESTO_PATH, "r", encoding="utf-8") as f:
                    self.system_instruction = f.read()
                print(f"📖 Unbiased Manifesto Loaded ({len(self.system_instruction.splitlines())} lines)")
            else:
                print("⚠️ Warning: config/unbiased_core.txt not found. Using default logic.")
                self.system_instruction = "You are a helpful AI assistant."
        except Exception as e:
            print(f"❌ Error loading manifesto: {e}")

        # 2. Connect to Ollama
        try:
            r = httpx.get(config.OLLAMA_URL, timeout=3)
            if r.status_code == 200:
                self.client = Client(host=config.OLLAMA_URL)
                print("✅ LLaMA connected")
        except Exception as e:
            print(f"❌ Model offline: {e}")

model = ModelManager()

# =========================
# UI COMPONENTS
# =========================
def safe_widget(name, cls):
    try:
        print(f"[UI] Loading {name}...")
        w = cls()
        print(f"[UI] {name} loaded ✅")
        return w
    except Exception as e:
        print(f"❌ {name} failed: {e}")
        return QTextEdit(f"{name} FAILED")

class Bridge(QObject):
    log_signal = pyqtSignal(str, str)

class VeronixOS(QMainWindow):
    def __init__(self, bridge):
        super().__init__()
        self.bridge = bridge
        self.setWindowTitle("VERONIX OS - UNBIASED CORE")
        self.setMinimumSize(1200, 850)
        
        try:
            self.setStyleSheet(get_stylesheet())
        except:
            print("[UI] Theme loading failed.")

        self._build_ui()

    def _build_ui(self):
        print("🧱 UI BUILD START")
        main_container = QWidget()
        layout = QVBoxLayout(main_container)
        v_splitter = QSplitter(Qt.Vertical)
        top_section = QSplitter(Qt.Horizontal)

        self.neural_monitor = safe_widget("NeuralMonitorPanel", NeuralMonitorPanel)
        self.screener = safe_widget("ScreenerPanel", ScreenerPanel)
        self.subsystems = safe_widget("SubsystemPanel", SubsystemPanel)

        top_section.addWidget(self.neural_monitor)
        top_section.addWidget(self.screener)
        top_section.addWidget(self.subsystems)
        top_section.setStretchFactor(1, 2) 

        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        self.console_display = QTextEdit("SYSTEM INITIALIZING...")
        self.console_display.setReadOnly(True)
        self.console_display.setStyleSheet("background-color: #050a0a; color: #00ffcc; font-family: 'Consolas', monospace;")
        
        self.keyboard = safe_widget("KeyboardWidget", KeyboardWidget)
        bottom_layout.addWidget(self.console_display)
        bottom_layout.addWidget(self.keyboard)

        v_splitter.addWidget(top_section)
        v_splitter.addWidget(bottom_widget)
        v_splitter.setStretchFactor(0, 3) 

        layout.addWidget(v_splitter)
        self.setCentralWidget(main_container)
        print("🧱 UI BUILD DONE ✅")

    @pyqtSlot(str, str)
    def update_console(self, source, message):
        self.console_display.append(f"<b><font color='#00ffff'>[{source}]</font></b> {message}")
        self.console_display.moveCursor(self.console_display.textCursor().End)

# =========================
# CORE AI ENGINE
# =========================
class VERONIX:
    def __init__(self, bridge):
        self.bridge = bridge
        self.stt = None
        self.tts = None
        self.q = queue.Queue()
        self.is_listening = False
        
        threading.Thread(target=self._init_systems, daemon=True).start()

    def _init_systems(self):
        time.sleep(1.0)
        print("[INIT] Booting Sensory Cores...")
        
        # 1. TTS First
        try:
            from sensory.voice import TTSEngine
            self.tts = TTSEngine()
        except Exception as e:
            print(f"❌ TTS Load Error: {e}")

        time.sleep(1.0) 
        print("[SYS] TTS Settled. Preparing STT...")

        # 2. STT Second (Wait for TTS to release audio handles)
        try:
            from sensory.listen import STTEngine
            self.stt = STTEngine()
            print("[SYS] STT Initialized. Stabilizing...")
        except Exception as e:
            print(f"❌ STT Load Error: {e}")
        
        # CRITICAL: Wait for the STT model AND its internal state to be stable
        if self.stt:
            print("[SYS] Waiting for STT background thread to stabilize...")
            time.sleep(3.0) 
            
        print("✅ Sensory Handshake Complete.")
        system_settled.set()

    def speak_worker(self):
        while not shutdown_event.is_set():
            try:
                msg = self.q.get(timeout=0.2)
                speaking_event.set()
                self.bridge.log_signal.emit("VERONIX", msg)
                if self.tts: self.tts.speak(msg)
                speaking_event.clear()
            except queue.Empty: continue

    def run(self):
        print("🚀 ENGINE ONLINE")
        
        # WAIT HERE: Do not proceed until sensors are stable
        system_settled.wait()

        # Ensure model is loaded
        while not model.client:
            time.sleep(0.5)

        self.bridge.log_signal.emit("SYSTEM", "VERONIX OS V1.0 ONLINE. UNBIASED CORE ACTIVE.")
        threading.Thread(target=self.speak_worker, daemon=True).start()

        # MAIN LOOP
        while not shutdown_event.is_set():
            if speaking_event.is_set():
                time.sleep(0.1)
                continue
                
            try:
                if self.stt and getattr(self.stt, 'model_ready', False) and not self.is_listening:
                    
                    self.is_listening = True
                    print("[SYS] Listening cycle started...")
                    
                    # Blocking call to STT
                    raw_text = self.stt.listen()
                    
                    self.is_listening = False
                    
                    # SANITIZATION: Handle empty returns from silence/timeout
                    if raw_text is None or not isinstance(raw_text, str):
                        print("[SYS] Invalid input type. Ignoring.")
                        time.sleep(1.0)
                        continue
                    
                    # Strip whitespace for checking
                    text = raw_text.strip()
                    
                    # If text is empty or placeholder (user didn't speak), ignore silently
                    if len(text) == 0 or text.lower() in ["result", "undefined", "null", "none", "placeholder_text"]:
                        # We don't print 'Ghost Input' here every time to reduce log spam if user is just quiet.
                        time.sleep(0.5)
                        continue
                    
                    # VALID SPEECH DETECTED
                    self.bridge.log_signal.emit("USER", text)
                    
                    if model.client:
                        res = model.client.chat(
                            model=config.MODEL, 
                            messages=[
                                {"role": "system", "content": model.system_instruction},
                                {"role": "user", "content": text}
                            ]
                        )
                        self.q.put(res["message"]["content"])
                    
                else:
                    time.sleep(0.5)
                    
            except Exception as e:
                self.is_listening = False
                print(f"⚠️ Engine Runtime Error: {e}")
                time.sleep(1)

# =========================
# EXECUTION
# =========================
def handler(sig, frame):
    shutdown_event.set()
    QApplication.quit()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    app = QApplication(sys.argv)
    
    bridge = Bridge()
    window = VeronixOS(bridge)
    bridge.log_signal.connect(window.update_console)

    window.show()
    QApplication.processEvents() 
    
    print("✅ GUI Window Active")
    model.init() 
    
    core = VERONIX(bridge) 
    threading.Thread(target=core.run, daemon=True).start()

    sys.exit(app.exec_())