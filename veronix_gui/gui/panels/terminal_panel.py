"""
VERONIX — Panel 1: Terminal Dashboard (PyQt5)
First screen the user sees.
Layout: Left sidebar | Center terminal | Right stats + globe
Bottom: Virtual keyboard
SCREENER button in top-bar switches to Panel 2.
"""
import math
import time
from collections import deque

import psutil
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPlainTextEdit, QLineEdit, QPushButton,
    QFrame, QSizePolicy, QScrollBar, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QPainter, QFontDatabase

from gui.panels.subsystem_sidebar import SubsystemSidebar


# ── log-level colors ──────────────────────────────────────────────────────────
LOG_COLORS = {
    "INFO":    "#00ffcc",
    "WARNING": "#ffaa00",
    "ERROR":   "#ff3b3b",
    "DEBUG":   "#888888",
}

# ── AGI commands ──────────────────────────────────────────────────────────────
COMMANDS = {
    "help": [
        "  VERONIX Shell — Available Commands",
        "  ─────────────────────────────────────",
        "  help         show this menu",
        "  clear        clear terminal",
        "  whoami       current user",
        "  uname -a     system info",
        "  ls [dir]     list files",
        "  ps           active processes",
        "  status       subsystem health",
        "  neofetch     full system overview",
        "  tree         project structure",
        "  kb           knowledge base stats",
        "  experts      loaded expert models",
        "  checkpoints  training checkpoints",
        "  ping         network test",
        "  date         current date/time",
        "  screener     launch SCREENER panel",
        "  echo [text]  print text",
    ],
    "whoami": ["root (VERONIX-01\\Administrator)"],
    "uname -a": ["VERONIX 5.15.0-AGI #1 SMP x86_64 Windows 10.0.26220"],
    "ls": [
        "D:\\AGI_Universal_Project\\",
        "  build_omni.py      MythosFriday_Core.py   NeoCore_Scientist.py",
        "  seed_brain.py      Knowledge_Audit.py     manifest.json",
        "  [AGI/]             [Brain_Data/]          [Datasets/]",
        "  [Experts/]         [Knowledge_Base/]      [Logs/]",
        "  [Models/]          [outputs/]             [Scripts/]",
        "  [Tools/]           [unsloth_compiled_cache/]",
    ],
    "ls scripts": [
        "D:\\AGI_Universal_Project\\Scripts\\",
        "  agi_router.py      Automation_Bridge.py   config.py",
        "  create_initial_dataset.py  download_model.py  generate_data.py",
        "  router.py          save_expert.py         stt_module.py",
        "  test_expert.py     train_expert.py        tts_module.py",
        "  Veronix_Auditor.py",
    ],
    "ls agi/core": [
        "D:\\AGI_Universal_Project\\AGI\\core\\",
        "  agent.py  brain.py  context.py  continuous_learning.py  debate.py",
        "  environment.py  goals.py  goal_system.py  identity.py  memory.py",
        "  online_model.py  planner.py  reward.py  scheduler.py",
        "  self_evolver.py  self_modify.py  state.py  tools.py",
        "  tool_runtime.py  world_model.py",
    ],
    "ls knowledge_base": [
        "D:\\AGI_Universal_Project\\Knowledge_Base\\  (342 files)",
        "  00_OMNI_BRAIN.md  Veronix_Core.md  AGI_Architecture.md",
        "  Master_Atlas.md   Neural_Networks.md  Quantum_Computing.md",
        "  Machine_Learning.md  Neuroscience.md  Reinforcement_Learning.md",
        "  ... (+333 more .md knowledge documents)",
    ],
    "ps": [
        "PID    CPU%   MEM%   STATUS    CMD",
        "────────────────────────────────────────────────────",
        "2201   14.2    9.1   RUNNING   MythosFriday_Core.py",
        "2204    5.8    6.3   RUNNING   NeoCore_Scientist.py",
        "2210    3.1    2.8   RUNNING   AGI/main.py",
        "2218    2.4    1.9   RUNNING   Scripts/router.py",
        "2225    1.7    1.4   RUNNING   Scripts/stt_module.py",
        "2231    1.2    1.1   RUNNING   Scripts/tts_module.py",
        "2238    0.8    0.6   RUNNING   Scripts/Automation_Bridge.py",
        "2245    0.3    0.4   RUNNING   Tools/Research_Bridge.py",
        "2250    0.0    0.2   IDLE      Scripts/train_expert.py",
    ],
    "status": [
        "VERONIX SUBSYSTEM HEALTH",
        "═══════════════════════════════",
        "  AGI/core          [ONLINE ]  brain.py + memory.py active",
        "  AGI/engine        [ONLINE ]  thinker.py + world_loop.py",
        "  AGI/io            [ONLINE ]  listen.py + voice.py",
        "  AGI/sandbox       [ONLINE ]  core.py + world_model.py",
        "  AGI/omniverse     [IDLE   ]  isaac_world.py not started",
        "  omniverse_bridge  [IDLE   ]  client.py disconnected",
        "  Scripts/router    [ONLINE ]  expert routing active",
        "  Scripts/stt       [ONLINE ]  mic input ready",
        "  Scripts/tts       [ONLINE ]  voice output ready",
        "  Experts/py_logic  [LOADED ]  adapter_model.safetensors",
        "  Brain_Data/mem0   [ONLINE ]  storage.sqlite connected",
        "  SCREENER          [ONLINE ]  neural terrain render active",
        "  outputs/ckpt-120  [SAVED  ]  latest checkpoint",
    ],
    "neofetch": [
        "",
        "    ##  ##   VERONIX / OMNI-BRAIN v3.0",
        "   ######   ─────────────────────────────────",
        "  ########  OS:       Windows 10 Build 26220.7523",
        "   ######   Host:     VERONIX-WORKSTATION-01",
        "    ##  ##  Kernel:   10.0.26220",
        "             Shell:    PowerShell 7.4",
        "             CPU:      Intel Core i9-13900K",
        "             GPU:      NVIDIA RTX 4090 24GB",
        "             RAM:      64 GB DDR5",
        "             Model:    Llama-3.2-1B-4bit",
        "             Expert:   Experts/python_logic",
        "             Brain:    Brain_Data/mem0 (SQLite)",
        "             KB:       342 knowledge documents",
        "             Ckpt:     outputs/checkpoint-120",
        "             TTS:      en_US-lessac-medium.onnx",
        "",
    ],
    "tree": [
        "D:\\AGI_Universal_Project\\",
        "├── AGI/         (core, engine, io, omniverse_bridge, rl, sandbox, vision)",
        "├── brain/       personality.py",
        "├── Brain_Data/  mem0 + mem0_entities (SQLite)",
        "├── Datasets/    python_logic.jsonl  python_logic_500.jsonl",
        "├── Experts/     python_logic/  sdr_expert/",
        "├── Knowledge_Base/  342 .md files",
        "├── Logs/",
        "├── Models/      Llama-3.2-1B-4bit/  en_US-lessac-medium.onnx",
        "├── outputs/     checkpoint-60/  checkpoint-120/",
        "├── Scripts/     13 scripts (stt, tts, router, train, audit...)",
        "├── Tools/       Knowledge_Deployer, Research_Bridge, tool_router",
        "├── unsloth_compiled_cache/  11 trainer files",
        "├── MythosFriday_Core.py",
        "└── NeoCore_Scientist.py",
    ],
    "kb": [
        "KNOWLEDGE BASE — D:\\AGI_Universal_Project\\Knowledge_Base\\",
        "──────────────────────────────────────────────────────────",
        "  Total files:  342 documents (.md)",
        "  Domains:      Physics, Medicine, Military, CS, Math,",
        "                Law, Biology, Philosophy, Economics...",
        "  Notable:      Veronix_Core.md, 00_OMNI_BRAIN.md,",
        "                Master_Atlas.md, AGI_Architecture.md",
        "  Tactical Briefs: 10 (2026-04-20 series)",
        "  Pillar files: 22 (AI_ML, Medicine, Law, Finance...)",
        "  Obsidian vault: .obsidian/ configured",
    ],
    "experts": [
        "LOADED EXPERT ADAPTERS",
        "──────────────────────────────────────",
        "  [1] Experts/python_logic/",
        "      adapter_model.safetensors  OK",
        "      tokenizer.json             OK",
        "",
        "  [2] Experts/sdr_expert/",
        "      (empty — not yet trained)",
        "",
        "  Base model: Models/Llama-3.2-1B-4bit",
        "  Framework:  Unsloth (unsloth_compiled_cache/)",
    ],
    "checkpoints": [
        "TRAINING CHECKPOINTS — outputs\\",
        "──────────────────────────────────────",
        "  [1] checkpoint-60",
        "      Step: 60   Loss: ~1.42",
        "",
        "  [2] checkpoint-120  [LATEST]",
        "      Step: 120  Loss: ~0.87",
        "",
        "  Dataset: python_logic_500.jsonl (500 samples)",
        "  Script:  Scripts/train_expert.py",
    ],
    "ping": [
        "Pinging localhost [127.0.0.1]:",
        "  Reply: time=0.3ms TTL=128",
        "  Reply: time=0.4ms TTL=128",
        "  Reply: time=0.3ms TTL=128",
        "Ping stats: 3 sent, 3 recv, 0% loss, avg=0.33ms",
    ],
    "screener": ["Launching SCREENER panel..."],
}


# ── Globe canvas widget ───────────────────────────────────────────────────────

class GlobeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(110, 110)
        self._angle = 0.0
        t = QTimer(self)
        t.timeout.connect(self._tick)
        t.start(40)

    def _tick(self):
        self._angle = (self._angle + 0.25) % 360
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        W, H, R, cx, cy = 110, 110, 52, 55, 55
        p.setBrush(QColor("#001a13"))
        p.setPen(QColor("#00ffcc44"))
        p.drawEllipse(cx - R, cy - R, R * 2, R * 2)

        for lat in range(-80, 90, 20):
            yr  = int(math.cos(math.radians(lat)) * R)
            yc  = int(cy + math.sin(math.radians(lat)) * R)
            p.setPen(QColor("#00ffcc18"))
            p.drawEllipse(cx - yr, yc - yr, yr * 2, yr * 2)

        for lng in range(0, 360, 30):
            a = math.radians(lng + self._angle)
            pts = []
            for lat in range(-85, 90, 6):
                la = math.radians(lat)
                x  = int(cx + R * math.cos(la) * math.sin(a))
                y  = int(cy + R * math.sin(la))
                z  = math.cos(la) * math.cos(a)
                if z > 0:
                    pts.append((x, y))
            if len(pts) > 1:
                p.setPen(QColor("#00ffcc18"))
                for i in range(len(pts) - 1):
                    p.drawLine(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1])

        conts = [
            [(0.3,0.35),(0.45,0.3),(0.5,0.45),(0.35,0.5),(0.25,0.42)],
            [(0.55,0.35),(0.65,0.3),(0.7,0.45),(0.6,0.5)],
            [(0.3,0.55),(0.42,0.52),(0.45,0.65),(0.32,0.68)],
            [(0.55,0.55),(0.7,0.5),(0.72,0.68),(0.57,0.7)],
        ]
        for cont in conts:
            pts = []
            for px, py in cont:
                lg = math.radians(px * 360 + self._angle)
                lt = math.radians(py * 180 - 90)
                x  = int(cx + R * math.cos(lt) * math.sin(lg))
                y  = int(cy + R * math.sin(lt))
                z  = math.cos(lt) * math.cos(lg)
                if z > 0:
                    pts.append((x, y))
            if len(pts) > 2:
                p.setBrush(QColor("#00ffcc55"))
                p.setPen(QColor("#00ffcc33"))
                from PyQt5.QtGui import QPolygon
                from PyQt5.QtCore import QPoint
                poly = QPolygon([QPoint(x, y) for x, y in pts])
                p.drawPolygon(poly)


# ── Right stats panel ─────────────────────────────────────────────────────────

class RightPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(130)
        self.setStyleSheet("background:#050d0b;")

        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(4)

        def sec(t):
            l = QLabel(t.upper())
            l.setStyleSheet("color:#00ffcc44;font-size:9px;letter-spacing:2px;"
                            "border-bottom:1px solid #1a3a2a;padding-bottom:3px;background:transparent;")
            return l

        def row(name):
            h = QHBoxLayout()
            h.setContentsMargins(0,0,0,0)
            n = QLabel(name)
            n.setStyleSheet("color:#00ffcc44;font-size:9px;background:transparent;")
            v = QLabel("--")
            v.setAlignment(Qt.AlignRight)
            v.setStyleSheet("color:#00ffcc;font-size:9px;background:transparent;")
            h.addWidget(n); h.addStretch(); h.addWidget(v)
            return h, v

        root.addWidget(sec("Globe"))
        self._globe = GlobeWidget()
        root.addWidget(self._globe)

        root.addWidget(sec("Network"))
        r, self._nu = row("UP");     root.addLayout(r)
        r, self._nd = row("DOWN");   root.addLayout(r)
        r, self._np = row("PING");   root.addLayout(r)
        r, self._pk = row("PKT");    root.addLayout(r)

        root.addWidget(sec("Build"))
        for n, v in [("OS","Win10 26220"),("GPU","RTX 4090"),
                     ("MODEL","Llama3.2"),("EXPERT","py_logic")]:
            rr, _ = row(n)
            _.setText(v); _.setStyleSheet("color:#00ffcc88;font-size:8px;background:transparent;")
            root.addLayout(rr)

        r, self._upt  = row("UPTIME"); root.addLayout(r)
        r, self._tmp  = row("TEMP");   root.addLayout(r)

        root.addWidget(sec("Brain Data"))
        for n, v in [("mem0","sqlite"),("entities","sqlite"),("CKPT","step-120")]:
            rr, _ = row(n)
            _.setText(v); _.setStyleSheet("color:#00ffcc88;font-size:9px;background:transparent;")
            root.addLayout(rr)

        root.addStretch()
        self._pkt_count = 0
        self._t0        = time.time()

        t = QTimer(self)
        t.timeout.connect(self._tick)
        t.start(1500)

    def _tick(self):
        import random
        self._nu.setText(f"{random.randint(100,600)} KB/s")
        self._nd.setText(f"{random.randint(400,2500)} KB/s")
        self._np.setText(f"{random.randint(8,40)} ms")
        self._pkt_count += random.randint(10, 150)
        self._pk.setText(f"{self._pkt_count:,}")
        up = int(time.time() - self._t0)
        self._upt.setText(f"{up//60}m {up%60}s" if up >= 60 else f"{up}s")
        self._tmp.setText(f"{random.randint(44,76)}°C")


# ── Keyboard widget ───────────────────────────────────────────────────────────

class VirtualKeyboard(QWidget):
    key_pressed = pyqtSignal(str)

    ROWS = [
        ["ESC","F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12","DEL"],
        ["`","1","2","3","4","5","6","7","8","9","0","-","=","BKSP"],
        ["TAB","Q","W","E","R","T","Y","U","I","O","P","[","]","\\"],
        ["CAPS","A","S","D","F","G","H","J","K","L",";","'","ENTER"],
        ["SHIFT","Z","X","C","V","B","N","M",",",".","/","SHIFT"],
        ["CTRL","WIN","ALT","SPACE","ALT","CTRL"],
    ]
    WIDE  = {"ESC","TAB","BKSP","CAPS","ENTER","DEL","\\"}
    WIDER = {"SHIFT","CTRL","WIN","ALT"}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background:#040c0a;border-top:1px solid #1a3a2a;")
        root = QVBoxLayout(self)
        root.setContentsMargins(6, 5, 6, 5)
        root.setSpacing(3)

        self._buttons = {}
        for row in self.ROWS:
            hl = QHBoxLayout()
            hl.setSpacing(2)
            for key in row:
                btn = QPushButton(key)
                base = (
                    "QPushButton{background:#0a1a15;color:#00ffcc77;"
                    "border:1px solid #1a3a2a;border-radius:2px;"
                    "font-size:9px;font-family:'Courier New';padding:3px 0px;"
                    "min-height:20px;}"
                    "QPushButton:hover{background:#0f2e22;color:#00ffcc;border-color:#00ffcc55;}"
                    "QPushButton:pressed{background:#00ffcc1a;color:#00ffcc;border-color:#00ffcc;}"
                )
                btn.setStyleSheet(base)
                if key == "SPACE":
                    btn.setMinimumWidth(140)
                elif key in self.WIDER:
                    btn.setMinimumWidth(46)
                elif key in self.WIDE:
                    btn.setMinimumWidth(38)
                else:
                    btn.setMinimumWidth(22)

                char = self._key_to_char(key)
                btn.clicked.connect(lambda _, k=key, c=char: self._on_click(k, c))
                hl.addWidget(btn)
                self._buttons[key] = btn

            if row == self.ROWS[-1]:
                pass
            root.addLayout(hl)

    def _key_to_char(self, key: str) -> str:
        mapping = {
            "SPACE": " ", "BKSP": "\b", "ENTER": "\n", "TAB": "\t",
            "ESC": "\x1b",
        }
        if key in mapping:
            return mapping[key]
        if len(key) == 1:
            return key.lower()
        return ""

    def _on_click(self, key: str, char: str):
        self.key_pressed.emit(key)

    def flash_key(self, key_name: str):
        k = key_name.upper()
        if k in self._buttons:
            btn = self._buttons[k]
            orig = btn.styleSheet()
            btn.setStyleSheet(orig.replace("#0a1a15", "#00ffcc22"))
            QTimer.singleShot(120, lambda: btn.setStyleSheet(orig))


# ── Terminal widget ───────────────────────────────────────────────────────────

class TerminalWidget(QWidget):
    launch_screener = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # header bar
        hdr = QFrame()
        hdr.setFixedHeight(22)
        hdr.setStyleSheet("background:#040c0a;border-bottom:1px solid #1a3a2a;")
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(10, 0, 10, 0)
        for txt in ["USER: root", "HOST: VERONIX-01",
                    "PATH: D:\\AGI_Universal_Project", "SHELL: PowerShell 7.4"]:
            l = QLabel(txt.split(":")[0] + ": ")
            l.setStyleSheet("color:#00ffcc44;font-size:9px;background:transparent;")
            v = QLabel(txt.split(": ", 1)[1])
            v.setStyleSheet("color:#00ffcc88;font-size:9px;background:transparent;")
            hl.addWidget(l); hl.addWidget(v); hl.addSpacing(12)
        hl.addStretch()
        root.addWidget(hdr)

        # output area
        self._output = QPlainTextEdit()
        self._output.setReadOnly(True)
        self._output.setStyleSheet(
            "background:#070d0d;color:#00ffcc99;border:none;"
            "font-family:'Courier New';font-size:11px;"
        )
        self._output.setMaximumBlockCount(2000)
        root.addWidget(self._output, 1)

        # input row
        inp_frame = QFrame()
        inp_frame.setFixedHeight(26)
        inp_frame.setStyleSheet("background:#040c0a;border-top:1px solid #1a3a2a;")
        il = QHBoxLayout(inp_frame)
        il.setContentsMargins(10, 0, 10, 0)
        self._prompt = QLabel("PS D:\\AGI>")
        self._prompt.setStyleSheet("color:#00ffcc;font-size:11px;background:transparent;")
        self._input  = QLineEdit()
        self._input.setStyleSheet(
            "background:transparent;border:none;color:#00ffcc;"
            "font-family:'Courier New';font-size:11px;"
        )
        il.addWidget(self._prompt); il.addWidget(self._input)
        root.addWidget(inp_frame)

        self._history = deque(maxlen=100)
        self._hist_idx = -1

        self._input.returnPressed.connect(self._execute)
        self._boot()

    def _boot(self):
        boot_lines = [
            ("VERONIX OMNI-BRAIN v3.0 — AGI UNIVERSAL PROJECT", "INFO"),
            ("Root: D:\\AGI_Universal_Project", "INFO"),
            ("Model: Llama-3.2-1B-4bit  |  Expert: python_logic  |  CKPT: 120", "INFO"),
            ("Brain: Brain_Data/mem0.sqlite  |  KB: 342 docs", "INFO"),
            ("All core subsystems ONLINE. Omniverse: IDLE.", "INFO"),
            ("─" * 56, "DEBUG"),
            ("Type 'help' for commands. Try: status, ps, neofetch, screener", "DEBUG"),
            ("", "DEBUG"),
        ]
        for line, level in boot_lines:
            self._append(line, level)

    def _append(self, text: str, level: str = "INFO"):
        from datetime import datetime
        ts   = datetime.now().strftime("%H:%M:%S")
        full = f"[{ts}] {text}" if text.strip() else ""
        self._output.appendPlainText(full if text.strip() else "")
        # color via cursor
        cursor = self._output.textCursor()
        cursor.movePosition(cursor.End)
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(LOG_COLORS.get(level, "#00ffcc99")))
        self._output.setCurrentCharFormat(fmt)

    def _execute(self):
        raw = self._input.text().strip()
        self._input.clear()
        if not raw:
            return
        self._history.appendleft(raw)
        self._hist_idx = -1
        self._output.appendPlainText(f"PS D:\\AGI> {raw}")

        if raw.lower() == "clear":
            self._output.clear()
            return

        if raw.lower() == "screener":
            self._append("Launching SCREENER panel...", "INFO")
            QTimer.singleShot(300, self.launch_screener.emit)
            return

        if raw.lower().startswith("echo "):
            self._append(raw[5:], "INFO")
            return

        if raw.lower() == "date":
            from datetime import datetime
            self._append(datetime.now().strftime("%A, %d %B %Y  %H:%M:%S"), "INFO")
            return

        key = raw.lower()
        if key in COMMANDS:
            for line in COMMANDS[key]:
                self._append(line, "INFO")
        else:
            self._append(f"'{raw.split()[0]}' is not recognized. Type 'help'.", "ERROR")

    def feed_key(self, key: str):
        """Receive virtual keyboard key press."""
        if key == "BKSP":
            txt = self._input.text()
            self._input.setText(txt[:-1])
        elif key == "ENTER":
            self._execute()
        elif key == "SPACE":
            self._input.setText(self._input.text() + " ")
        elif key == "TAB":
            self._input.setText(self._input.text() + "  ")
        elif len(key) == 1:
            self._input.setText(self._input.text() + key.lower())
        self._input.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            if self._hist_idx < len(self._history) - 1:
                self._hist_idx += 1
                self._input.setText(self._history[self._hist_idx])
        elif event.key() == Qt.Key_Down:
            if self._hist_idx > 0:
                self._hist_idx -= 1
                self._input.setText(self._history[self._hist_idx])
            else:
                self._hist_idx = -1
                self._input.clear()
        else:
            super().keyPressEvent(event)


# ── Panel 1 main widget ───────────────────────────────────────────────────────

class TerminalPanel(QWidget):
    """
    Panel 1 — full VERONIX terminal interface.
    Emits `launch_screener` signal when user types 'screener' or clicks button.
    """
    launch_screener = pyqtSignal()

    def __init__(self, sidebar: SubsystemSidebar, parent=None):
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── top bar ───────────────────────────────────────────────────────────
        topbar = QFrame()
        topbar.setFixedHeight(30)
        topbar.setStyleSheet("background:#050a0a;border-bottom:1px solid #00ffcc33;")
        tl = QHBoxLayout(topbar)
        tl.setContentsMargins(10, 0, 10, 0)

        logo = QLabel("VERONIX")
        logo.setStyleSheet("color:#00ffcc;font-size:13px;font-weight:bold;letter-spacing:4px;background:transparent;")
        sub  = QLabel("OMNI-BRAIN v3.0")
        sub.setStyleSheet("color:#00ffcc44;font-size:9px;letter-spacing:2px;background:transparent;")

        self._clock = QLabel("00:00:00")
        self._clock.setStyleSheet("color:#00ffcc;font-size:16px;font-weight:bold;letter-spacing:2px;background:transparent;")

        # SCREENER button
        self._btn_screener = QPushButton("⬡  SCREENER")
        self._btn_screener.setObjectName("btn_screener")
        self._btn_screener.setFixedHeight(22)
        self._btn_screener.clicked.connect(self.launch_screener.emit)

        # status dots
        def dot_row(color, text):
            w = QWidget(); w.setStyleSheet("background:transparent;")
            hl = QHBoxLayout(w); hl.setContentsMargins(0,0,0,0); hl.setSpacing(3)
            d = QLabel("●")
            d.setStyleSheet(f"color:{color};font-size:8px;background:transparent;")
            t = QLabel(text)
            t.setStyleSheet("color:#00ffcc88;font-size:9px;background:transparent;")
            hl.addWidget(d); hl.addWidget(t)
            return w

        tl.addWidget(logo); tl.addSpacing(6); tl.addWidget(sub)
        tl.addStretch()
        tl.addWidget(self._clock)
        tl.addStretch()
        tl.addWidget(dot_row("#00ffcc", "AGI/CORE"))
        tl.addWidget(dot_row("#00ffcc", "MEMORY"))
        tl.addWidget(dot_row("#ffaa00", "OMNIVERSE"))
        tl.addSpacing(12)
        tl.addWidget(self._btn_screener)
        self._date_lbl = QLabel("")
        self._date_lbl.setStyleSheet("color:#00ffcc44;font-size:9px;background:transparent;margin-left:8px;")
        tl.addWidget(self._date_lbl)

        root.addWidget(topbar)

        # ── body ──────────────────────────────────────────────────────────────
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        body.addWidget(sidebar)

        # center: terminal
        self._terminal = TerminalWidget()
        self._terminal.launch_screener.connect(self.launch_screener.emit)
        body.addWidget(self._terminal, 1)

        # right stats
        self._right = RightPanel()
        body.addWidget(self._right)

        body_w = QWidget()
        body_w.setLayout(body)
        root.addWidget(body_w, 1)

        # ── keyboard ──────────────────────────────────────────────────────────
        self._kbd = VirtualKeyboard()
        self._kbd.key_pressed.connect(self._terminal.feed_key)
        root.addWidget(self._kbd)

        # clock timer
        t = QTimer(self)
        t.timeout.connect(self._tick_clock)
        t.start(1000)
        self._tick_clock()

    def _tick_clock(self):
        from datetime import datetime
        n = datetime.now()
        self._clock.setText(n.strftime("%H:%M:%S"))
        self._date_lbl.setText(n.strftime("%a %d %b %Y"))

    def update_metrics(self, m: dict):
        pass  # sidebar already connected in app_window