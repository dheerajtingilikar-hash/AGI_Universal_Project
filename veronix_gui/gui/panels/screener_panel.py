"""
VERONIX — Panel 2: SCREENER (PyQt5)
Data Sequence Analysis — Neural Terrain Heatmap.
Shows animated 3D isometric terrain with heatmap colouring,
particle flow lines, orbital rings, and live data readouts.
← BACK button returns to Panel 1.
"""
import math
import time
import random

import numpy as np
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSizePolicy, QGridLayout,
    QProgressBar
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPolygon, QFont
from PyQt5.QtCore import QPoint

from gui.panels.subsystem_sidebar import SubsystemSidebar


# ── Heat colour map (blue→teal→green→yellow→orange→red) ──────────────────────
def heat_color(t: float):
    t = max(0.0, min(1.0, t))
    if t < 0.20: r = t / 0.20; return (0,               int(60+r*160),  int(r*100))
    if t < 0.40: r=(t-0.20)/0.20; return (0,             int(220+r*35),  int(100-r*100))
    if t < 0.60: r=(t-0.40)/0.20; return (int(r*255),    255,            0)
    if t < 0.80: r=(t-0.60)/0.20; return (255,           int(255-r*165), 0)
    r=(t-0.80)/0.20;              return (255,            int(90-r*50),   int(r*60))


# ── Terrain canvas ─────────────────────────────────────────────────────────────
class TerrainCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(280)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.COLS = 38
        self.ROWS = 26
        self._t   = 0.0
        self._particles = []
        for _ in range(40):
            self._particles.append({
                "x":  random.uniform(0, self.COLS),
                "y":  random.uniform(0, self.ROWS),
                "vx": random.uniform(-0.35, 0.35),
                "vy": random.uniform(-0.25, 0.25),
                "life": random.random(),
            })

        # live readouts (updated by paintEvent)
        self.freq  = 0.0
        self.amp   = 0.0
        self.delta = 0.0
        self.peak  = 0.0

        t = QTimer(self)
        t.timeout.connect(self._tick)
        t.start(22)          # ~45 FPS

    def _tick(self):
        self._t += 0.016
        # advance particles
        for p in self._particles:
            p["x"] += p["vx"] + math.sin(p["y"] * 0.4 + self._t) * 0.12
            p["y"] += p["vy"] + math.cos(p["x"] * 0.3 + self._t) * 0.10
            p["life"] += 0.005
            if (p["x"] < 0 or p["x"] > self.COLS or
                    p["y"] < 0 or p["y"] > self.ROWS or p["life"] > 1.0):
                p["x"]   = random.uniform(0, self.COLS)
                p["y"]   = random.uniform(0, self.ROWS)
                p["vx"]  = random.uniform(-0.35, 0.35)
                p["vy"]  = random.uniform(-0.25, 0.25)
                p["life"]= 0.0
        self.update()

    # ── terrain height function ────────────────────────────────────────────────
    def _h(self, x, y):
        nx, ny = x / self.COLS, y / self.ROWS
        t = self._t
        return (math.sin(nx * 3.4 + t * 0.65) * 0.30 +
                math.sin(ny * 2.9 - t * 0.55) * 0.25 +
                math.sin((nx + ny) * 4.2 + t * 0.90) * 0.20 +
                math.sin(nx * 6.1 - ny * 2.1 + t * 1.1) * 0.12 +
                math.cos(ny * 5.0 + nx * 1.6 - t * 0.60) * 0.13)

    # ── isometric projection ───────────────────────────────────────────────────
    def _iso(self, cx, cy, x, y, h, cell_w, cell_h):
        px = cx + (x - y) * cell_w * 0.90
        py = cy + (x + y) * cell_h - h * 55
        return int(px), int(py)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        W = self.width()
        H = self.height()
        painter.fillRect(0, 0, W, H, QColor("#020808"))

        cell_w = W / (self.COLS + 4)
        cell_h = H * 0.021
        ox     = W * 0.50
        oy     = H * 0.26

        # pre-compute heights
        heights = [[self._h(x, y) for x in range(self.COLS + 1)]
                   for y in range(self.ROWS + 1)]

        peak = 0.0
        # draw back-to-front
        for y in range(self.ROWS - 1, -1, -1):
            for x in range(self.COLS - 1, -1, -1):
                h00 = heights[y][x]
                h10 = heights[y][x + 1]
                h01 = heights[y + 1][x]
                h11 = heights[y + 1][x + 1]
                avg  = (h00 + h10 + h01 + h11) / 4.0
                norm = (avg + 1.0) / 2.0
                if avg > peak:
                    peak = avg

                r, g, b = heat_color(norm)
                p0 = self._iso(ox, oy, x,   y,   h00, cell_w, cell_h)
                p1 = self._iso(ox, oy, x+1, y,   h10, cell_w, cell_h)
                p2 = self._iso(ox, oy, x+1, y+1, h11, cell_w, cell_h)
                p3 = self._iso(ox, oy, x,   y+1, h01, cell_w, cell_h)

                poly = QPolygon([QPoint(*p0), QPoint(*p1),
                                 QPoint(*p2), QPoint(*p3)])
                painter.setBrush(QBrush(QColor(r, g, b, 210)))
                edge_r = min(r + 30, 255)
                edge_g = min(g + 30, 255)
                edge_b = min(b + 30, 255)
                painter.setPen(QPen(QColor(edge_r, edge_g, edge_b, 50), 0.4))
                painter.drawPolygon(poly)

        # particles
        for p in self._particles:
            px, py = self._iso(ox, oy, p["x"], p["y"],
                               self._h(p["x"], p["y"]), cell_w, cell_h)
            alpha = int(abs(math.sin(p["life"] * math.pi)) * 180)
            painter.setBrush(QBrush(QColor(255, 255, 255, alpha)))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(px - 1, py - 1, 3, 3)

            # trail
            px2, py2 = self._iso(ox, oy,
                                  p["x"] - p["vx"] * 5,
                                  p["y"] - p["vy"] * 5,
                                  self._h(p["x"], p["y"]), cell_w, cell_h)
            painter.setPen(QPen(QColor(255, 255, 255, alpha // 4), 0.8))
            painter.drawLine(px, py, px2, py2)

        # orbital rings
        ring_cx = int(ox)
        ring_cy = int(oy + H * 0.06)
        ring_r1 = int(min(W, H) * 0.44)
        ring_r2 = int(min(W, H) * 0.52)
        painter.setPen(QPen(QColor(0, 255, 200, 40), 1.5))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(ring_cx - ring_r1, ring_cy - ring_r1,
                            ring_r1 * 2, ring_r1 * 2)
        painter.setPen(QPen(QColor(0, 255, 200, 18), 0.7))
        painter.drawEllipse(ring_cx - ring_r2, ring_cy - ring_r2,
                            ring_r2 * 2, ring_r2 * 2)

        # scan line effect (subtle)
        painter.setPen(QPen(QColor(0, 255, 200, 6), 1))
        for yl in range(0, H, 4):
            painter.drawLine(0, yl, W, yl)

        # update live stats
        self.freq  = 1.2 + math.sin(self._t * 0.3) * 0.4
        self.amp   = (peak + 1.0)
        self.delta = 8.0 + random.random() * 4.0
        self.peak  = peak * 100


# ── Signal data bar row ────────────────────────────────────────────────────────
def _sig_row(label: str, color: str):
    h = QHBoxLayout()
    h.setContentsMargins(0, 0, 0, 0)
    h.setSpacing(5)
    lbl = QLabel(label)
    lbl.setFixedWidth(40)
    lbl.setStyleSheet(f"color:{color}55;font-size:9px;background:transparent;")
    bar = QProgressBar()
    bar.setRange(0, 100)
    bar.setValue(0)
    bar.setTextVisible(False)
    bar.setFixedHeight(4)
    bar.setStyleSheet(f"QProgressBar{{background:#001a13;border:none;}}"
                      f"QProgressBar::chunk{{background:{color};}}")
    h.addWidget(lbl)
    h.addWidget(bar, 1)
    return h, bar


# ── Left data panel ────────────────────────────────────────────────────────────
class LeftDataPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(180)
        self.setStyleSheet("background:#030d0a;border-right:1px solid #1a3a2a;")

        root = QVBoxLayout(self)
        root.setContentsMargins(8, 10, 8, 10)
        root.setSpacing(6)

        def sec(t):
            l = QLabel(t)
            l.setStyleSheet("color:#00ffcc44;font-size:9px;letter-spacing:2px;"
                            "border-bottom:1px solid #1a3a2a;padding-bottom:3px;"
                            "background:transparent;")
            return l

        def stat_row(name, val="--"):
            h = QHBoxLayout(); h.setContentsMargins(0,0,0,0)
            n = QLabel(name); n.setStyleSheet("color:#00ffcc44;font-size:9px;background:transparent;")
            v = QLabel(val);  v.setStyleSheet("color:#00ffcc;font-size:9px;background:transparent;")
            v.setAlignment(Qt.AlignRight)
            h.addWidget(n); h.addStretch(); h.addWidget(v)
            return h, v

        root.addWidget(sec("DATA SEQUENCE ANALYSIS"))

        r, self._freq  = stat_row("FREQUENCY"); root.addLayout(r)
        r, self._amp   = stat_row("AMPLITUDE"); root.addLayout(r)
        r, self._nodes = stat_row("NODES", "988"); root.addLayout(r)
        r, self._delta = stat_row("DELTA"); root.addLayout(r)
        r, self._fps   = stat_row("RENDER FPS", "45"); root.addLayout(r)

        root.addSpacing(4)
        root.addWidget(sec("SEQUENCE INDEX"))
        sig_r, self._sig_a = _sig_row("SIG-A", "#00ffcc"); root.addLayout(sig_r)
        sig_r, self._sig_b = _sig_row("SIG-B", "#ffaa00"); root.addLayout(sig_r)
        sig_r, self._sig_c = _sig_row("SIG-C", "#ff3b3b"); root.addLayout(sig_r)

        root.addSpacing(4)
        root.addWidget(sec("NEURAL SOURCE"))
        for name, val in [("brain.py","ONLINE"),("memory.py","ONLINE"),
                          ("stt_module","ACTIVE"),("tts_module","ACTIVE")]:
            r, v = stat_row(name, val)
            color = "#00ffcc" if val in ("ONLINE","ACTIVE") else "#ffaa00"
            v.setStyleSheet(f"color:{color};font-size:9px;background:transparent;")
            root.addLayout(r)

        root.addSpacing(4)
        root.addWidget(sec("TERRAIN CONFIG"))
        for name, val in [("GRID","38 x 26"),("PARTICLES","40"),
                          ("WAVES","4 freq."),("PROJECTION","ISO")]:
            r, v = stat_row(name, val)
            v.setStyleSheet("color:#00ffcc88;font-size:9px;background:transparent;")
            root.addLayout(r)

        root.addStretch()

        t = QTimer(self)
        t.timeout.connect(self._tick)
        t.start(800)

    def _tick(self):
        self._sig_a.setValue(random.randint(40, 95))
        self._sig_b.setValue(random.randint(20, 75))
        self._sig_c.setValue(random.randint(10, 60))

    def update_stats(self, freq, amp, delta, peak):
        self._freq.setText(f"{freq:.2f} Hz")
        self._amp.setText(f"{amp:.2f}")
        self._delta.setText(f"{delta:.2f} ms")


# ── Right data panel ───────────────────────────────────────────────────────────
class RightDataPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(160)
        self.setStyleSheet("background:#030d0a;border-left:1px solid #1a3a2a;")

        root = QVBoxLayout(self)
        root.setContentsMargins(8, 10, 8, 10)
        root.setSpacing(6)

        def sec(t):
            l = QLabel(t)
            l.setStyleSheet("color:#00ffcc44;font-size:9px;letter-spacing:2px;"
                            "border-bottom:1px solid #1a3a2a;padding-bottom:3px;"
                            "background:transparent;")
            return l

        def stat_row(name, val="--"):
            h = QHBoxLayout(); h.setContentsMargins(0,0,0,0)
            n = QLabel(name); n.setStyleSheet("color:#00ffcc44;font-size:9px;background:transparent;")
            v = QLabel(val);  v.setStyleSheet("color:#00ffcc;font-size:9px;background:transparent;")
            v.setAlignment(Qt.AlignRight)
            h.addWidget(n); h.addStretch(); h.addWidget(v)
            return h, v

        root.addWidget(sec("SYSTEM STATUS"))
        for name, val, color in [
            ("AGI/core",   "ONLINE",  "#00ffcc"),
            ("brain.py",   "ONLINE",  "#00ffcc"),
            ("omniverse",  "IDLE",    "#ffaa00"),
            ("SCREENER",   "ACTIVE",  "#00ff88"),
            ("router.py",  "ONLINE",  "#00ffcc"),
        ]:
            r, v = stat_row(name, val)
            v.setStyleSheet(f"color:{color};font-size:9px;font-weight:bold;background:transparent;")
            root.addLayout(r)

        root.addSpacing(4)
        root.addWidget(sec("SIGNAL METRICS"))
        r, self._peak = stat_row("PEAK"); root.addLayout(r)
        r, self._rms  = stat_row("RMS");  root.addLayout(r)
        r, self._snr  = stat_row("SNR");  root.addLayout(r)

        root.addSpacing(4)
        root.addWidget(sec("RENDER ENGINE"))
        for name, val in [("MODE","ISOMETRIC"),("SHADING","HEATMAP"),
                          ("CMAP","SPECTRAL"),("BLEND","ALPHA 0.88")]:
            r, v = stat_row(name, val)
            v.setStyleSheet("color:#00ffcc88;font-size:8px;background:transparent;")
            root.addLayout(r)

        root.addSpacing(4)
        root.addWidget(sec("MEMORY"))
        r, self._mem_cpu = stat_row("CPU MEM"); root.addLayout(r)
        r, self._mem_gpu = stat_row("GPU MEM"); root.addLayout(r)

        root.addStretch()

        t = QTimer(self)
        t.timeout.connect(self._tick)
        t.start(900)

    def _tick(self):
        self._peak.setText(f"{random.randint(60,99)}%")
        self._rms.setText(f"{random.uniform(0.3,0.8):.2f}")
        self._snr.setText(f"{random.uniform(18,40):.1f} dB")
        self._mem_cpu.setText(f"{random.randint(3,8)} GB")
        self._mem_gpu.setText(f"{random.randint(6,18)} GB")


# ── Panel 2 main widget ────────────────────────────────────────────────────────
class ScreenerPanel(QWidget):
    """
    Panel 2 — SCREENER data-sequence analysis view.
    Emits `go_back` to return to Panel 1.
    """
    go_back = pyqtSignal()

    def __init__(self, sidebar: SubsystemSidebar, parent=None):
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── top bar ───────────────────────────────────────────────────────────
        topbar = QFrame()
        topbar.setFixedHeight(30)
        topbar.setStyleSheet("background:#030d0a;border-bottom:1px solid #00ffcc44;")
        tl = QHBoxLayout(topbar)
        tl.setContentsMargins(10, 0, 10, 0)
        tl.setSpacing(10)

        # back button
        btn_back = QPushButton("◀  BACK")
        btn_back.setObjectName("btn_back")
        btn_back.setFixedHeight(22)
        btn_back.clicked.connect(self.go_back.emit)
        tl.addWidget(btn_back)

        title = QLabel("SCREENER")
        title.setStyleSheet("color:#00ffcc;font-size:14px;font-weight:bold;"
                            "letter-spacing:5px;background:transparent;")
        sub = QLabel("DATA SEQUENCE ANALYSIS — NEURAL TERRAIN MAP")
        sub.setStyleSheet("color:#00ffcc55;font-size:9px;letter-spacing:1px;background:transparent;")

        tl.addWidget(title)
        tl.addWidget(sub)
        tl.addStretch()

        # live readouts in top bar
        self._freq_lbl  = QLabel("FREQ: 0.00 Hz")
        self._amp_lbl   = QLabel("AMP: 0.00")
        self._nodes_lbl = QLabel("NODES: 988")
        self._delta_lbl = QLabel("DELTA: 0.00 ms")
        for lbl in (self._freq_lbl, self._amp_lbl,
                    self._nodes_lbl, self._delta_lbl):
            lbl.setStyleSheet("color:#00ffcc88;font-size:9px;"
                              "border:1px solid #1a3a2a;padding:1px 6px;"
                              "background:#050d0b;")
            tl.addWidget(lbl)

        self._clock = QLabel("00:00:00")
        self._clock.setStyleSheet("color:#00ffcc;font-size:14px;font-weight:bold;"
                                  "letter-spacing:2px;background:transparent;")
        tl.addWidget(self._clock)

        root.addWidget(topbar)

        # ── body row ──────────────────────────────────────────────────────────
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        body.addWidget(sidebar)

        # center: terrain
        self._canvas = TerrainCanvas()
        body.addWidget(self._canvas, 1)

        # right panel
        self._right_data = RightDataPanel()
        body.addWidget(self._right_data)

        body_w = QWidget()
        body_w.setLayout(body)
        root.addWidget(body_w, 1)

        # ── bottom status bar ─────────────────────────────────────────────────
        bot = QFrame()
        bot.setFixedHeight(22)
        bot.setStyleSheet("background:#030d0a;border-top:1px solid #1a3a2a;")
        bl = QHBoxLayout(bot)
        bl.setContentsMargins(10, 0, 10, 0)
        bl.setSpacing(20)
        for txt in ["MODE: NEURAL TERRAIN", "GRID: 38×26",
                    "PARTICLES: 40", "PROJECTION: ISOMETRIC",
                    "COLOR MAP: SPECTRAL", "RENDER: REALTIME"]:
            l = QLabel(txt)
            l.setStyleSheet("color:#00ffcc33;font-size:9px;background:transparent;")
            bl.addWidget(l)
        bl.addStretch()
        self._peak_bar_lbl = QLabel("PEAK: 0%")
        self._peak_bar_lbl.setStyleSheet("color:#ff6644;font-size:9px;background:transparent;")
        bl.addWidget(self._peak_bar_lbl)
        root.addWidget(bot)

        # clock timer
        clk = QTimer(self)
        clk.timeout.connect(self._tick_clock)
        clk.start(1000)
        self._tick_clock()

        # stats update timer
        stats_t = QTimer(self)
        stats_t.timeout.connect(self._tick_stats)
        stats_t.start(300)

    def _tick_clock(self):
        from datetime import datetime
        self._clock.setText(datetime.now().strftime("%H:%M:%S"))

    def _tick_stats(self):
        freq  = self._canvas.freq
        amp   = self._canvas.amp
        delta = self._canvas.delta
        peak  = self._canvas.peak

        self._freq_lbl.setText(f"FREQ: {freq:.2f} Hz")
        self._amp_lbl.setText(f"AMP: {amp:.2f}")
        self._delta_lbl.setText(f"DELTA: {delta:.2f} ms")
        self._peak_bar_lbl.setText(f"PEAK: {peak:.0f}%")
        self._right_data._tick()