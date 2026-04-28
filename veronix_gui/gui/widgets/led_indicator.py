"""
VERONIX — LED Indicator Widget (PyQt5)
"""
import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor


class LEDIndicator(QWidget):
    STATE_ONLINE   = "online"
    STATE_DEGRADED = "degraded"
    STATE_OFFLINE  = "offline"

    _COLORS = {
        STATE_ONLINE:   "#00ffcc",
        STATE_DEGRADED: "#ffaa00",
        STATE_OFFLINE:  "#ff3b3b",
    }

    def __init__(self, parent=None, size: int = 9):
        super().__init__(parent)
        self._size  = size
        self._state = self.STATE_ONLINE
        self._alpha = 255
        self._phase = 0.0
        self.setFixedSize(size + 6, size + 6)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(40)

    def set_state(self, state: str):
        self._state = state
        self.update()

    def _tick(self):
        if self._state != self.STATE_OFFLINE:
            self._phase = (self._phase + 0.12) % (2 * math.pi)
            self._alpha = int(140 + 115 * abs(math.sin(self._phase)))
        else:
            self._alpha = 160
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        color = QColor(self._COLORS[self._state])
        r  = self._size // 2
        cx = self.width()  // 2
        cy = self.height() // 2

        glow = QColor(color)
        glow.setAlpha(25)
        p.setBrush(glow)
        p.setPen(Qt.NoPen)
        p.drawEllipse(cx - r - 3, cy - r - 3, (r + 3) * 2, (r + 3) * 2)

        color.setAlpha(self._alpha)
        p.setBrush(color)
        p.setPen(Qt.NoPen)
        p.drawEllipse(cx - r, cy - r, r * 2, r * 2)