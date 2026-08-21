from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QProgressBar
)
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal

# Corrected Imports to match your folder structure
from . import Theme as T
from .Led_indicator import LEDIndicator
from .Process_worker import ProcessWorker
from .Metrics_worker import SystemMetrics

PROJECT_ROOT = Path(r"D:\AGI_Universal_Project")

# Subsystem registry: name → script path relative to project root
SUBSYSTEMS = [
    ("AGI/core",      "AGI/main.py"),
    ("MythosFriday",    "MythosFriday_Core.py"),
    ("NeoCore_Sci",     "NeoCore_Scientist.py"),
    ("brain.py",        "AGI/core/brain.py"),
    ("memory.py",       "AGI/core/memory.py"),
    ("omniverse",       "AGI/omniverse_bridge/loop.py"),
    ("stt_module",      "Scripts/stt_module.py"),
    ("tts_module",      "Scripts/tts_module.py"),
    ("router.py",       "Scripts/router.py"),
    ("SCREENER",        None),   # internal widget — no subprocess
    ("train_expert",    "Scripts/train_expert.py"),
]

class SubsystemCard(QFrame):
    restart_requested = pyqtSignal(str)
    kill_requested    = pyqtSignal(str)

    def __init__(self, name: str, script: str, parent=None):
        super().__init__(parent)
        self.name = name
        self.script = script
        self._state = "offline"
        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background:{T.BG_ELEVATED};
                border:1px solid {T.BORDER_DEFAULT};
                border-radius:2px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(2)

        row1 = QHBoxLayout()
        row1.setSpacing(5)

        self._led = LEDIndicator("offline", size=8)
        row1.addWidget(self._led)

        lbl_name = QLabel(self.name)
        lbl_name.setStyleSheet(f"font-size:9px;color:{T.ACCENT_CYAN_MID};")
        row1.addWidget(lbl_name, 1)

        self._lbl_status = QLabel("OFFLINE")
        self._lbl_status.setObjectName("status-offline")
        row1.addWidget(self._lbl_status)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(4)

        # CPU Bar
        self._cpu_bar = QProgressBar()
        self._cpu_bar.setRange(0, 100)
        self._cpu_bar.setFixedHeight(3)
        self._cpu_bar.setTextVisible(False)
        self._cpu_bar.setStyleSheet(f"QProgressBar {{ background:#001a13; border:none; }} QProgressBar::chunk {{ background:{T.ACCENT_CYAN}; }}")

        # RAM Bar
        self._ram_bar = QProgressBar()
        self._ram_bar.setRange(0, 100)
        self._ram_bar.setFixedHeight(3)
        self._ram_bar.setTextVisible(False)
        self._ram_bar.setStyleSheet(f"QProgressBar {{ background:#001a13; border:none; }} QProgressBar::chunk {{ background:{T.COLOR_WARN}; }}")

        row2.addWidget(QLabel("C"), 0)
        row2.addWidget(self._cpu_bar, 1)
        row2.addWidget(QLabel("R"), 0)
        row2.addWidget(self._ram_bar, 1)
        layout.addLayout(row2)

        if self.script:
            row3 = QHBoxLayout()
            btn_restart = QPushButton("RESTART")
            btn_restart.setFixedHeight(16)
            btn_restart.clicked.connect(lambda: self.restart_requested.emit(self.name))

            btn_kill = QPushButton("KILL")
            btn_kill.setFixedHeight(16)
            btn_kill.clicked.connect(lambda: self.kill_requested.emit(self.name))

            row3.addWidget(btn_restart)
            row3.addWidget(btn_kill)
            layout.addLayout(row3)

    def set_state(self, state: str):
        self._state = state
        self._led.set_state(state)
        labels = {
            "online":  ("ONLINE",   "status-online"),
            "offline": ("OFFLINE",  "status-offline"),
            "warn":    ("DEGRADED", "status-warn"),
            "idle":    ("IDLE",     "status-warn"),
        }
        text, obj_name = labels.get(state, ("UNKNOWN", "status-offline"))
        self._lbl_status.setText(text)

    def set_metrics(self, cpu: float, ram: float):
        self._cpu_bar.setValue(int(cpu))
        self._ram_bar.setValue(int(ram))


class SubsystemPanel(QWidget):
    log_line = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(160)
        self.setStyleSheet(f"background:{T.BG_SURFACE};")
        self._cards = {}
        self._workers = {}
        self._build_ui()
        self._init_workers()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        hdr = QFrame()
        hdr.setFixedHeight(28)
        hdr_layout = QHBoxLayout(hdr)
        lbl = QLabel("SUBSYSTEMS")
        lbl.setStyleSheet(f"font-size:9px; letter-spacing:2px; color:{T.ACCENT_CYAN}; font-weight:bold;")
        hdr_layout.addWidget(lbl)
        layout.addWidget(hdr)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        container = QWidget()
        container.setStyleSheet("background:transparent;")
        self.card_layout = QVBoxLayout(container)
        self.card_layout.setContentsMargins(6, 6, 6, 6)
        self.card_layout.setSpacing(4)

        for name, script in SUBSYSTEMS:
            card = SubsystemCard(name, script)
            card.restart_requested.connect(self._on_restart)
            card.kill_requested.connect(self._on_kill)
            if script is None: card.set_state("online")
            self.card_layout.addWidget(card)
            self._cards[name] = card

        self.card_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll, 1)

    def _init_workers(self):
        for name, script in SUBSYSTEMS:
            if script is None: continue
            worker = ProcessWorker(name=name, script_path=str(PROJECT_ROOT / script))
            worker.line_received.connect(lambda line, lvl, n=name: self.log_line.emit(f"[{n}] {line}", lvl))
            worker.status_changed.connect(self._on_status_changed)
            self._workers[name] = worker

    @pyqtSlot(str, str)
    def _on_status_changed(self, name: str, status: str):
        if name in self._cards: self._cards[name].set_state(status)

    @pyqtSlot(str)
    def _on_restart(self, name: str):
        if name in self._workers:
            self._workers[name].restart_process()
            self.log_line.emit(f"[SYSTEM] Restarting {name}...", "SYS")

    @pyqtSlot(str)
    def _on_kill(self, name: str):
        if name in self._workers:
            self._workers[name].kill_process()
            self.log_line.emit(f"[SYSTEM] Killed {name}.", "WARN")

    @pyqtSlot(object)
    def on_metrics_updated(self, metrics: SystemMetrics):
        import random
        for name in self._cards:
            cpu = random.uniform(1, 15)
            ram = random.uniform(1, 10)
            self._cards[name].set_metrics(cpu, ram)

    def start_all(self):
        for w in self._workers.values(): w.start_process()

    def stop_all(self):
        for w in self._workers.values(): w.stop_process()