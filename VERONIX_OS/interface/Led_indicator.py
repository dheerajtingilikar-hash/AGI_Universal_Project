"""
LED Indicator Widget
Animated pulsing LED dot for subsystem status display.
"""

import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush


class LEDIndicator(QWidget):
    """
    Animated LED status indicator.
    States: online (cyan pulse), warn (amber solid), offline (red solid), idle (gray).
    """

    STATES = {
        "online":  {"color": QColor("#00ffcc"), "pulse": True},
        "warn":    {"color": QColor("#ffaa00"), "pulse": False},
        "offline": {"color": QColor("#ff3b3b"), "pulse": False},
        "idle":    {"color": QColor("#555555"), "pulse": False},
    }

    def __init__(self, state: str = "offline", size: int = 10, parent=None):
        super().__init__(parent)
        self._size = size
        self._state = state
        self._pulse_alpha = 1.0
        self._pulse_dir = -1
        self.setFixedSize(size + 6, size + 6)

        self._timer = QTimer(self)
        self._timer.setInterval(30)
        self._timer.timeout.connect(self._animate)
        self._timer.start()

    def set_state(self, state: str):
        if state in self.STATES:
            self._state = state
            self.update()

    def _animate(self):
        cfg = self.STATES.get(self._state, self.STATES["offline"])
        if cfg["pulse"]:
            self._pulse_alpha += self._pulse_dir * 0.03
            if self._pulse_alpha <= 0.3:
                self._pulse_dir = 1
            elif self._pulse_alpha >= 1.0:
                self._pulse_dir = -1
        else:
            self._pulse_alpha = 1.0
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        cfg = self.STATES.get(self._state, self.STATES["offline"])
        color = QColor(cfg["color"])
        cx = self.width() // 2
        cy = self.height() // 2
        r = self._size // 2

        # Outer glow ring (only for online/pulsing)
        if cfg["pulse"]:
            glow = QColor(cfg["color"])
            glow.setAlphaF(self._pulse_alpha * 0.25)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(glow))
            p.drawEllipse(cx - r - 3, cy - r - 3, (r + 3) * 2, (r + 3) * 2)

        # Main dot
        color.setAlphaF(self._pulse_alpha if cfg["pulse"] else 1.0)
        p.setBrush(QBrush(color))
        border_color = QColor(cfg["color"])
        border_color.setAlphaF(0.5)
        p.setPen(QPen(border_color, 1))
        p.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        p.end()