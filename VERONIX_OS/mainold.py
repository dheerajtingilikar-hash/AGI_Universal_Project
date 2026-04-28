import os
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
# WINDOWS FIX
# =========================
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# =========================
# PATH FIX
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSplitter, QTextEdit, QLabel
from PyQt5.QtCore import Qt, QObject, pyqtSlot, pyqtSignal

# Custom modules
from interface.Theme import get_stylesheet
from interface.Neural_monitor import NeuralMonitorPanel
from interface.Subsystem_panel import SubsystemPanel
from interface.Screener_panel import ScreenerPanel
from interface.Keyboard_widget import KeyboardWidget

shutdown_event = threading.Event()
speaking_event = threading.Event()

# =========================
# CONFIG
# =========================
@dataclass
class Config:
    OLLAMA_URL: str = "http://127.0.0.1:11434"
    MODEL: str = "llama3.2:3b"

config = Config()

# =========================
# BRIDGE
# =========================
class Bridge(QObject):
    log_signal = pyqtSignal(str, str)

# =========================
# MODEL
# =========================
class ModelManager:
    def __init__(self):
        self.client = None

    def init(self):
        try:
            r = httpx.get(config.OLLAMA_URL, timeout=3)
            if r.status_code == 200:
                self.client = Client(host=config.OLLAMA_URL)
                print("✅ LLaMA connected")
        except Exception as e:
            print(f"❌ Model offline: {e}")

model = ModelManager()

# =========================
# SAFE WIDGET LOADER
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

# =========================
# UI
# =========================
class VeronixOS(QMainWindow):
    def __init__(self, bridge):
        super().__init__()
        self.bridge = bridge

        self.setWindowTitle("VERONIX OS")
        self.setMinimumSize(1200, 850)
        
        try:
            self.setStyleSheet(get_stylesheet())
        except Exception as e:
            print(f"[UI] Theme error: {e}")

        self._build_ui()

    def _build_ui(self):
        print("🧱 UI BUILD START")

        main_container = QWidget()
        layout = QVBoxLayout(main_container)

        v_splitter = QSplitter(Qt.Vertical)
        top_section = QSplitter(Qt.Horizontal)

        # Panels
        self.neural_monitor = safe_widget("NeuralMonitorPanel", NeuralMonitorPanel)
        self.screener = safe_widget("ScreenerPanel", ScreenerPanel)
        self.subsystems = safe_widget("SubsystemPanel", SubsystemPanel)

        top_section.addWidget(self.neural_monitor)
        top_section.addWidget(self.screener)
        top_section.addWidget(self.subsystems)

        # 🎯 FIX 1: Added to define width
        top_section.setSizes()
        top_section.setStretchFactor(0, 1)
        top_section.setStretchFactor(1, 2)
        top_section.setStretchFactor(2, 1)

        # Bottom
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)

        self.console_display = QTextEdit("SYSTEM READY...")
        self.console_display.setReadOnly(True)
        self.console_display.setStyleSheet("""
            background-color: #070d0d;
            color: #00ffcc;
            border: 1px solid #00ffcc22;
            font-family: 'JetBrains Mono', Consolas;
            font-size: 11px;
        """)

        self.keyboard = safe_widget("KeyboardWidget", KeyboardWidget)

        bottom_layout.addWidget(self.console_display)
        bottom_layout.addWidget(self.keyboard)

        v_splitter.addWidget(top_section)
        v_splitter.addWidget(bottom_widget)

        # 🎯 FIX 2: Added to define height
        v_splitter.setSizes()
        v_splitter.setStretchFactor(0, 3)
        v_splitter.setStretchFactor(1, 1)

        layout.addWidget(v_splitter)
        self.setCentralWidget(main_container)

        print("🧱 UI BUILD DONE ✅")

    @pyqtSlot(str, str)
    def update_console(self, source, message):
        self.console_display.append(f"[{source}] >> {message}")
        self.console_display.moveCursor(self.console_display.textCursor().End)

# =========================
# CORE ENGINE
# =========================
class VERONIX:
    def __init__(self, bridge):
        self.bridge = bridge
        self.stt = None
        self.tts = None
        self.q = queue.Queue()
        threading.Thread(target=self._init_systems, daemon=True).start()

    def _init_systems(self):
        print("[INIT] Loading STT + TTS...")
        def load_stt():
            try:
                from sensory.listen import STTEngine
                self.stt = STTEngine()
            except Exception as e:
                print(f"❌ STT failed: {e}")

        def load_tts():
            try:
                from sensory.voice import TTSEngine
                self.tts = TTSEngine()
            except Exception as e:
                print(f"❌ TTS failed: {e}")

        threading.Thread(target=load_stt, daemon=True).start()
        threading.Thread(target=load_tts, daemon=True).start()

    def speak_worker(self):
        while not shutdown_event.is_set():
            try:
                msg = self.q.get(timeout=0.2)
                speaking_event.set()
                self.bridge.log_signal.emit("VERONIX", msg)
                if self.tts:
                    self.tts.speak(msg)
                speaking_event.clear()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ TTS Worker Error: {e}")
                speaking_event.clear()

    def run(self):
        print("🚀 ENGINE ONLINE")
        self.q.put("VERONIX OS V1.0 INITIALIZED.")
        threading.Thread(target=self.speak_worker, daemon=True).start()

        while not shutdown_event.is_set():
            if not self.stt:
                time.sleep(0.2)
                continue
            if speaking_event.is_set():
                time.sleep(0.1)
                continue
            try:
                text = self.stt.listen()
                if text:
                    self.bridge.log_signal.emit("USER", text)
                    if model.client:
                        res = model.client.chat(
                            model=config.MODEL,
                            messages=[{"role": "user", "content": text}]
                        )
                        reply = res["message"]["content"]
                    else:
                        reply = "Ollama connection lost."
                    self.q.put(reply)
                else:
                    time.sleep(0.1)
            except Exception as e:
                print(f"⚠️ Runtime error: {e}")
                time.sleep(1)

# =========================
# MAIN
# =========================
def handler(sig, frame):
    print("\n🛑 Shutting down VERONIX...")
    shutdown_event.set()
    QApplication.quit()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    print("🚀 Booting VERONIX OS...")
    model.init()
    app = QApplication(sys.argv)
    bridge = Bridge()
    window = VeronixOS(bridge)
    bridge.log_signal.connect(window.update_console)
    window.show()
    window.raise_()
    window.activateWindow()
    print("✅ GUI Window displayed")
    core = VERONIX(bridge)
    threading.Thread(target=core.run, daemon=True).start()
    sys.exit(app.exec_())