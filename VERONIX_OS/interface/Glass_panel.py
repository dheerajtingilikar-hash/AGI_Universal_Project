"""
QFrame subclass with cyber-industrial border styling.
"""
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt


class GlassPanel(QFrame):
    """Styled panel container with optional title bar."""

    def __init__(self, parent=None, title: str = ""):
        super().__init__(parent)
        self.setObjectName("panel")
        self.setFrameShape(QFrame.StyledPanel)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        if title:
            self._header = QFrame(self)
            self._header.setFixedHeight(22)
            self._header.setStyleSheet(
                "QFrame { background: #050d0b; border: none;"
                "border-bottom: 1px solid #1a3a2a; }"
            )
            hl = QHBoxLayout(self._header)
            hl.setContentsMargins(8, 0, 8, 0)

            lbl = QLabel(title.upper())
            lbl.setStyleSheet(
                "color: #00ffcc44; font-size: 9px; letter-spacing: 2px;"
                "background: transparent; border: none;"
            )
            hl.addWidget(lbl)
            hl.addStretch()
            self._layout.addWidget(self._header)

        self._body = QFrame(self)
        self._body.setStyleSheet("QFrame { border: none; background: transparent; }")
        self._body_layout = QVBoxLayout(self._body)
        self._body_layout.setContentsMargins(6, 6, 6, 6)
        self._body_layout.setSpacing(4)
        self._layout.addWidget(self._body)

    def body_layout(self) -> QVBoxLayout:
        return self._body_layout

    def add_widget(self, widget):
        self._body_layout.addWidget(widget)

    def add_stretch(self):
        self._body_layout.addStretch()