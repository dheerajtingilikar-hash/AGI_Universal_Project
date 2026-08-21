"""
VERONIX — SCREENER Panel
3D isometric terrain heatmap with animated heatmap colors and particle flow lines.
Rendered with QPainter at 60 FPS via QTimer.
"""

import math
import time
import random
from dataclasses import dataclass

# Converted from PyQt6 to PyQt5
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QProgressBar
from PyQt5.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPolygonF, QLinearGradient, QPainterPath

# Fixed Import to point to local Theme.py
from . import Theme as T

COLS = 35
ROWS = 25
MAX_PARTICLES = 32

@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: float
    max_life: float

def heat_color(t: float) -> QColor:
    """Map 0.0–1.0 to heatmap color: dark-teal → green → yellow → orange → red."""
    t = max(0.0, min(1.0, t))
    if t < 0.15:
        r = t / 0.15
        return QColor(0, int(60 + r * 120), int(r * 80))
    if t < 0.35:
        r = (t - 0.15) / 0.20
        return QColor(0, int(180 + r * 75), int(80 - r * 80))
    if t < 0.55:
        r = (t - 0.35) / 0.20
        return QColor(int(r * 220), 255, 0)
    if t < 0.75:
        r = (t - 0.55) / 0.20
        return QColor(220 + int(r * 35), int(255 - r * 155), 0)
    r = (t - 0.75) / 0.25
    return QColor(255, int(100 - r * 60), int(r * 40))

def terrain_height(x: float, y: float, t: float) -> float:
    """Multi-frequency sine wave terrain."""
    nx, ny = x / COLS, y / ROWS
    return (
        math.sin(nx * 3.2 + t * 0.7) * 0.30 +
        math.sin(ny * 2.8 - t * 0.5) * 0.25 +
        math.sin((nx + ny) * 4.1 + t * 0.9) * 0.18 +
        math.sin(nx * 6.0 - ny * 2.0 + t * 1.1) * 0.12 +
        math.cos(ny * 5.0 + nx * 1.5 - t * 0.6) * 0.10
    )

class ScreenerCanvas(QWidget):
    """Raw canvas for SCREENER terrain rendering."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._time = 0.0
        self._particles: list[Particle] = []
        self._heights: list[list[float]] = [[0.0] * COLS for _ in range(ROWS)]
        self._peak = 0.0

        # Stat labels
        self.freq_val = 1.2
        self.amp_val = 0.0
        self.delta_val = 8.0
        self.nodes_val = COLS * ROWS

        self._init_particles()

        self._timer = QTimer(self)
        self._timer.setInterval(16)   # ~60 FPS
        self._timer.timeout.connect(self._tick)
        self._timer.start()

        self.setMinimumHeight(210)

    def _init_particles(self):
        for _ in range(MAX_PARTICLES):
            self._particles.append(Particle(
                x=random.uniform(0, COLS),
                y=random.uniform(0, ROWS),
                vx=random.uniform(-0.4, 0.4),
                vy=random.uniform(-0.3, 0.3),
                life=random.uniform(0, 1),
                max_life=random.uniform(0.6, 1.0),
            ))

    def _tick(self):
        self._time += 0.018
        self._update_particles()
        self.update()

    def _update_particles(self):
        t = self._time
        for p in self._particles:
            p.x += p.vx + math.sin(p.y * 0.4 + t) * 0.12
            p.y += p.vy + math.cos(p.x * 0.3 + t) * 0.10
            p.life += 0.007
            if p.x < 0 or p.x > COLS or p.y < 0 or p.y > ROWS or p.life > p.max_life:
                p.x = random.uniform(0, COLS)
                p.y = random.uniform(0, ROWS)
                p.vx = random.uniform(-0.4, 0.4)
                p.vy = random.uniform(-0.3, 0.3)
                p.life = 0.0
                p.max_life = random.uniform(0.6, 1.0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) # PyQt5 Syntax

        W, H = self.width(), self.height()
        painter.fillRect(0, 0, W, H, QColor("#020808"))

        t = self._time

        # Projection helpers
        cell_w = W / (COLS + 4)
        cell_h = H * 0.022
        ox = W * 0.5
        oy = H * 0.26

        def iso_x(cx, cy): return ox + (cx - cy) * cell_w * 0.95
        def iso_y(cx, cy, h): return oy + (cx + cy) * cell_h - h * 52

        # Build height map
        peak = 0.0
        for row in range(ROWS):
            for col in range(COLS):
                h = terrain_height(col, row, t)
                self._heights[row][col] = h
                if h > peak:
                    peak = h
        self._peak = peak

        # Draw terrain quads back-to-front
        painter.setPen(Qt.NoPen)
        for row in range(ROWS - 1, -1, -1):
            for col in range(COLS - 1, -1, -1):
                h00 = self._heights[row][col]
                h10 = self._heights[row][col + 1] if col < COLS - 1 else h00
                h01 = self._heights[row + 1][col] if row < ROWS - 1 else h00
                h11 = self._heights[row + 1][col + 1] if (col < COLS - 1 and row < ROWS - 1) else h00

                avg_h = (h00 + h10 + h01 + h11) / 4.0
                norm = (avg_h + 1.0) / 2.0

                color = heat_color(norm)
                color.setAlpha(220)

                p0 = QPointF(iso_x(col,   row),   iso_y(col,   row,   h00))
                p1 = QPointF(iso_x(col+1, row),   iso_y(col+1, row,   h10))
                p2 = QPointF(iso_x(col+1, row+1), iso_y(col+1, row+1, h11))
                p3 = QPointF(iso_x(col,   row+1), iso_y(col,   row+1, h01))

                poly = QPolygonF([p0, p1, p2, p3])
                painter.setBrush(QBrush(color))
                painter.drawPolygon(poly)

                # Grid edge lines
                edge_color = QColor(color)
                edge_color.setAlpha(40)
                pen = QPen(edge_color, 0.4)
                painter.setPen(pen)
                painter.setBrush(Qt.NoBrush)
                painter.drawPolygon(poly)
                painter.setPen(Qt.NoPen)

        # Orbital rings
        pen_ring = QPen(QColor(0, 255, 200, 35), 1.5)
        painter.setPen(pen_ring)
        painter.setBrush(Qt.NoBrush)
        r1 = min(W, H) * 0.44
        painter.drawEllipse(QRectF(ox - r1, oy + H * 0.04 - r1, r1 * 2, r1 * 2))

        pen_ring2 = QPen(QColor(0, 255, 200, 18), 0.8)
        painter.setPen(pen_ring2)
        r2 = min(W, H) * 0.53
        painter.drawEllipse(QRectF(ox - r2, oy + H * 0.04 - r2, r2 * 2, r2 * 2))

        # Particles
        for p in self._particles:
            h_at = terrain_height(p.x, p.y, t)
            px = iso_x(p.x, p.y)
            py = iso_y(p.x, p.y, h_at)
            alpha = math.sin(p.life / p.max_life * math.pi) * 0.75

            if alpha > 0.1:
                px2 = iso_x(p.x - p.vx * 4, p.y - p.vy * 4)
                py2 = iso_y(p.x - p.vx * 4, p.y - p.vy * 4, h_at)
                trail_color = QColor(255, 255, 255, int(alpha * 0.25 * 255))
                painter.setPen(QPen(trail_color, 0.8))
                painter.drawLine(QPointF(px, py), QPointF(px2, py2))

            dot_color = QColor(255, 255, 255, int(alpha * 255))
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(dot_color))
            painter.drawEllipse(QPointF(px, py), 1.3, 1.3)

        self.freq_val = 1.2 + math.sin(t * 0.3) * 0.4
        self.amp_val = (peak + 1.0)
        self.delta_val = 8.0 + random.uniform(0, 4)

        painter.end()

    def stop(self):
        self._timer.stop()

class ScreenerPanel(QWidget):
    """
    Full SCREENER panel with header stats bar + terrain canvas + signal index bars.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("panel-frame")
        self._build_ui()

        self._stats_timer = QTimer(self)
        self._stats_timer.setInterval(200)
        self._stats_timer.timeout.connect(self._refresh_stats)
        self._stats_timer.start()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        hdr = QFrame()
        hdr.setObjectName("top-bar")
        hdr.setFixedHeight(30)
        hdr_layout = QHBoxLayout(hdr)
        hdr_layout.setContentsMargins(10, 0, 10, 0)

        title_col = QVBoxLayout()
        title_col.setSpacing(0)
        lbl_title = QLabel("SCREENER")
        lbl_title.setStyleSheet(f"font-size:11px;letter-spacing:3px;color:{T.ACCENT_CYAN};font-weight:bold;")
        lbl_sub = QLabel("DATA SEQUENCE ANALYSIS — NEURAL TERRAIN MAP")
        lbl_sub.setStyleSheet(f"font-size:8px;color:{T.TEXT_MUTED};")
        title_col.addWidget(lbl_title)
        title_col.addWidget(lbl_sub)

        hdr_layout.addLayout(title_col)
        hdr_layout.addStretch()

        self._lbl_freq  = self._make_stat("FREQ",  "1.20 Hz")
        self._lbl_amp   = self._make_stat("AMP",   "0.00")
        self._lbl_nodes = self._make_stat("NODES", f"{COLS*ROWS}")
        self._lbl_delta = self._make_stat("DELTA", "8.00 ms")

        for w in [self._lbl_freq, self._lbl_amp, self._lbl_nodes, self._lbl_delta]:
            hdr_layout.addWidget(w)

        layout.addWidget(hdr)

        self._canvas = ScreenerCanvas(self)
        layout.addWidget(self._canvas)

        sig_bar = QFrame()
        sig_bar.setStyleSheet(f"background:{T.BG_INPUT};border-top:1px solid {T.BORDER_DEFAULT};")
        sig_bar.setFixedHeight(26)
        sig_layout = QHBoxLayout(sig_bar)
        sig_layout.setContentsMargins(10, 0, 10, 0)
        sig_layout.setSpacing(16)

        self._sig_a = self._make_sigbar("SIG-A", T.ACCENT_CYAN, sig_layout)
        self._sig_b = self._make_sigbar("SIG-B", T.COLOR_WARN,  sig_layout)
        self._sig_c = self._make_sigbar("SIG-C", T.COLOR_DANGER, sig_layout)
        sig_layout.addStretch()

        fps_lbl = QLabel("FPS: 60")
        fps_lbl.setStyleSheet(f"font-size:8px;color:{T.TEXT_MUTED};")
        self._fps_lbl = fps_lbl
        sig_layout.addWidget(fps_lbl)

        layout.addWidget(sig_bar)

    def _make_stat(self, key: str, val: str) -> QLabel:
        lbl = QLabel(f"{key}: {val}")
        lbl.setStyleSheet(f"font-size:8px;color:{T.TEXT_MUTED};padding:0 8px;")
        return lbl

    def _make_sigbar(self, name: str, color: str, layout):
        row = QHBoxLayout()
        row.setSpacing(4)
        lbl = QLabel(name)
        lbl.setStyleSheet(f"font-size:8px;color:{T.TEXT_MUTED};min-width:36px;")
        bar = QProgressBar()
        bar.setFixedSize(70, 4)
        bar.setRange(0, 100)
        bar.setValue(50)
        bar.setTextVisible(False)
        bar.setStyleSheet(f"""
            QProgressBar {{ background:#001a13; border:1px solid {T.BORDER_DEFAULT}; border-radius:0; }}
            QProgressBar::chunk {{ background:{color}; }}
        """)
        row.addWidget(lbl)
        row.addWidget(bar)
        layout.addLayout(row)
        return bar

    def _refresh_stats(self):
        c = self._canvas
        self._lbl_freq.setText(f"FREQ: {c.freq_val:.2f} Hz")
        self._lbl_amp.setText(f"AMP:  {c.amp_val:.2f}")
        self._lbl_delta.setText(f"DELTA: {c.delta_val:.2f} ms")

        self._sig_a.setValue(random.randint(40, 95))
        self._sig_b.setValue(random.randint(20, 70))
        self._sig_c.setValue(random.randint(10, 55))

    def stop(self):
        self._stats_timer.stop()
        self._canvas.stop()