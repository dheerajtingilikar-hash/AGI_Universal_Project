
import math
from collections import deque

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen


class CognitionPulse(QWidget):
    """Scrolling waveform widget driven by amplitude signal."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(48)
        self._amplitude   = 0.0          # 0.0 – 1.0
        self._phase       = 0.0
        self._samples     = deque(maxlen=200)
        self._active      = False

        for _ in range(200):
            self._samples.append(0.0)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)

    # ── public API ─────────────────
    def set_amplitude(self, amp: float) -> None:
        """Feed audio amplitude (0.0–1.0)."""
        self._amplitude = max(0.0, min(1.0, amp))
        self._active    = self._amplitude > 0.01

    def set_active(self, active: bool) -> None:
        self._active = active

    # ── internal ──────────────────────────────────────────────────────────────
    def _tick(self):
        self._phase += 0.18
        if self._active:
            a   = self._amplitude
            val = (math.sin(self._phase * 1.3) * 0.5 +
                   math.sin(self._phase * 2.7) * 0.3 +
                   math.sin(self._phase * 4.1) * 0.2) * a
        else:
            val = math.sin(self._phase * 0.4) * 0.04
        self._samples.append(val)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("#070d0d"))

        w = self.width()
        h = self.height()
        mid = h / 2

        samples = list(self._samples)
        n       = len(samples)
        if n < 2:
            return

        step = w / n
        pen  = QPen(QColor("#00ffcc"), 1.0)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        # centre line
        dim_pen = QPen(QColor("#00ffcc22"), 1)
        painter.setPen(dim_pen)
        painter.drawLine(0, int(mid), w, int(mid))

        painter.setPen(pen)
        for i in range(1, n):
            x1 = (i - 1) * step
            x2 = i * step
            y1 = mid - samples[i - 1] * (h * 0.45)
            y2 = mid - samples[i]     * (h * 0.45)
            # fade alpha by distance from right edge
            alpha = max(40, int(255 * (i / n)))
            c = QColor("#00ffcc")
            c.setAlpha(alpha)
            painter.setPen(QPen(c, 1.0))
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))