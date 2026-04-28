"""
VERONIX — Subsystem Sidebar (PyQt5)
Left panel shared by Panel 1 and Panel 2.
Shows CPU, RAM, subsystem LEDs, active processes, disk I/O.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QProgressBar, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt

from gui.widgets.led_indicator import LEDIndicator


# ── helpers ──────────────────────────────────────────────────────────────────

def _sep():
    f = QFrame()
    f.setFrameShape(QFrame.HLine)
    f.setStyleSheet("color: #1a3a2a; background: #1a3a2a; max-height:1px; border:none;")
    return f


def _section_label(text: str) -> QLabel:
    lbl = QLabel(text.upper())
    lbl.setObjectName("muted")
    lbl.setStyleSheet(
        "color:#00ffcc44; font-size:9px; letter-spacing:2px;"
        "border-bottom:1px solid #1a3a2a; padding-bottom:3px;"
        "background:transparent;"
    )
    return lbl


def _stat_row(name: str):
    row = QHBoxLayout()
    row.setContentsMargins(0, 0, 0, 0)
    name_lbl  = QLabel(name)
    name_lbl.setStyleSheet("color:#00ffcc77; font-size:9px; background:transparent;")
    value_lbl = QLabel("--")
    value_lbl.setAlignment(Qt.AlignRight)
    value_lbl.setStyleSheet("color:#00ffcc; font-size:9px; background:transparent;")
    row.addWidget(name_lbl)
    row.addStretch()
    row.addWidget(value_lbl)
    return row, value_lbl


def _bar(obj_name: str = "") -> QProgressBar:
    b = QProgressBar()
    b.setRange(0, 100)
    b.setValue(0)
    b.setTextVisible(False)
    b.setFixedHeight(5)
    if obj_name:
        b.setObjectName(obj_name)
    return b


# ── Subsystem row ─────────────────────────────────────────────────────────────

class SubsystemRow(QWidget):
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 1, 0, 1)
        layout.setSpacing(5)

        self.led    = LEDIndicator(self, size=7)
        self.name   = QLabel(name)
        self.name.setStyleSheet("color:#00ffcc88; font-size:9px; background:transparent;")
        self.status = QLabel("ON")
        self.status.setStyleSheet("color:#00ffcc; font-size:8px; font-weight:bold; background:transparent;")
        self.status.setAlignment(Qt.AlignRight)

        layout.addWidget(self.led)
        layout.addWidget(self.name, 1)
        layout.addWidget(self.status)

    def set_online(self):
        self.led.set_state(LEDIndicator.STATE_ONLINE)
        self.status.setText("ON")
        self.status.setStyleSheet("color:#00ffcc; font-size:8px; font-weight:bold; background:transparent;")

    def set_degraded(self):
        self.led.set_state(LEDIndicator.STATE_DEGRADED)
        self.status.setText("IDLE")
        self.status.setStyleSheet("color:#ffaa00; font-size:8px; font-weight:bold; background:transparent;")

    def set_offline(self):
        self.led.set_state(LEDIndicator.STATE_OFFLINE)
        self.status.setText("OFF")
        self.status.setStyleSheet("color:#ff3b3b; font-size:8px; font-weight:bold; background:transparent;")


# ── Main sidebar widget ───────────────────────────────────────────────────────

class SubsystemSidebar(QWidget):
    """Left sidebar showing metrics and subsystem health."""

    SUBSYSTEMS = [
        "AGI/core", "brain.py", "memory.py",
        "omniverse", "stt_module", "tts_module",
        "router.py", "SCREENER",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(148)
        self.setStyleSheet("background:#050d0b;")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(4)

        # ── CPU ──────────────────────────────────────────────────────────────
        root.addWidget(_section_label("CPU — i9-13900K"))
        self._core_bars = []
        self._core_vals = []
        for i in range(4):
            r, v = _stat_row(f"Core {i}")
            b    = _bar()
            root.addLayout(r)
            root.addWidget(b)
            self._core_vals.append(v)
            self._core_bars.append(b)

        root.addWidget(_sep())

        # ── Memory ───────────────────────────────────────────────────────────
        root.addWidget(_section_label("Memory — 64 GB"))
        r_ram, self._ram_val   = _stat_row("RAM")
        r_vram, self._vram_val = _stat_row("VRAM")
        _, self._used_val = _stat_row("Used")
        r_used = _
        _, self._free_val = _stat_row("Free")
        r_free = _
        self._ram_bar  = _bar("warn")
        self._vram_bar = _bar()
        root.addLayout(r_ram);  root.addWidget(self._ram_bar)
        root.addLayout(r_vram); root.addWidget(self._vram_bar)
        root.addLayout(r_used)
        root.addLayout(r_free)

        root.addWidget(_sep())

        # ── Subsystems ───────────────────────────────────────────────────────
        root.addWidget(_section_label("Subsystems"))
        self._sub_rows = {}
        for name in self.SUBSYSTEMS:
            row = SubsystemRow(name)
            self._sub_rows[name] = row
            root.addWidget(row)
            if name == "omniverse":
                row.set_degraded()

        root.addWidget(_sep())

        # ── Processes ────────────────────────────────────────────────────────
        root.addWidget(_section_label("Active Procs"))
        self._proc_labels = []
        for _ in range(5):
            r, v = _stat_row("--")
            root.addLayout(r)
            self._proc_labels.append((r, v))

        root.addWidget(_sep())

        # ── Disk I/O ─────────────────────────────────────────────────────────
        root.addWidget(_section_label("Disk I/O"))
        rd, self._dread_val  = _stat_row("Read")
        rw, self._dwrite_val = _stat_row("Write")
        self._dread_bar  = _bar()
        self._dwrite_bar = _bar("warn")
        root.addLayout(rd); root.addWidget(self._dread_bar)
        root.addLayout(rw); root.addWidget(self._dwrite_bar)

        root.addStretch()

    # ── public: receive metrics dict from MetricsWorker ──────────────────────
    def update_metrics(self, m: dict):
        cores = m.get("cpu_cores", [])
        for i, b in enumerate(self._core_bars):
            v = int(cores[i]) if i < len(cores) else 0
            b.setValue(v)
            self._core_vals[i].setText(f"{v}%")
            if v > 80:
                b.setObjectName("hot")
            elif v > 60:
                b.setObjectName("warn")
            else:
                b.setObjectName("")
            b.setStyleSheet(b.styleSheet())  # force refresh

        ram  = int(m.get("ram_pct", 0))
        vram = min(100, int(m.get("cpu_total", 0)))  # approximation
        self._ram_bar.setValue(ram)
        self._vram_bar.setValue(vram)
        self._ram_val.setText(f"{ram}%")
        self._vram_val.setText(f"{vram}%")
        self._used_val.setText(f"{m.get('ram_used_gb', 0):.1f} GB")
        self._free_val.setText(f"{m.get('ram_free_gb', 0):.1f} GB")

        dr = m.get("disk_read",  0.0)
        dw = m.get("disk_write", 0.0)
        self._dread_val.setText(f"{dr:.1f} MB/s")
        self._dwrite_val.setText(f"{dw:.1f} MB/s")
        self._dread_bar.setValue(min(100, int(dr * 2)))
        self._dwrite_bar.setValue(min(100, int(dw * 4)))

    def update_processes(self, procs: list):
        """procs: list of (name, cpu_pct) tuples, max 5."""
        for i, (r_layout, val_lbl) in enumerate(self._proc_labels):
            if i < len(procs):
                name, pct = procs[i]
                # find name label in layout
                item = r_layout.itemAt(0)
                if item and item.widget():
                    item.widget().setText(name[:12])
                val_lbl.setText(f"{pct:.1f}%")
            else:
                item = r_layout.itemAt(0)
                if item and item.widget():
                    item.widget().setText("--")
                val_lbl.setText("--")