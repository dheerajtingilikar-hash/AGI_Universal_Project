"""
Neural Monitor Panel
Real-time log streaming console with color coding, search, and auto-scroll.
Connects to ProcessWorker via Qt signals.
"""

from collections import deque
from datetime import datetime

# UPDATED: Framework changed to PyQt5
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QLineEdit, QLabel, QPushButton, QFrame, QCheckBox, QFileDialog
)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat, QFont

# FIX: Relative import to find the Theme file in the current package
from . import Theme as T

MAX_LINES = 10_000

LEVEL_COLORS = {
    "INFO":  T.ACCENT_CYAN_MID,
    "WARN":  T.COLOR_WARN,
    "ERROR": T.COLOR_DANGER,
    "DEBUG": "#666666",
    "OK":    T.COLOR_ONLINE,
    "SYS":   T.TEXT_INFO,
}

class NeuralMonitorPanel(QWidget):
    """
    Live log console.
    - Circular buffer: max 10,000 lines
    - Color-coded by log level
    - Timestamped entries
    - Auto-scroll toggle
    - Keyword filter
    - Export to file
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._buffer = deque(maxlen=MAX_LINES)
        self._filter_text = ""
        self._auto_scroll = True
        self._build_ui()

    # ── UI Construction ────────────────────────

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        hdr = QFrame()
        hdr.setObjectName("top-bar")
        hdr.setFixedHeight(28)
        hdr_layout = QHBoxLayout(hdr)
        hdr_layout.setContentsMargins(8, 0, 8, 0)
        hdr_layout.setSpacing(6)

        lbl = QLabel("NEURAL MONITOR")
        lbl.setStyleSheet(f"font-size:10px;letter-spacing:3px;color:{T.ACCENT_CYAN};font-weight:bold;")
        hdr_layout.addWidget(lbl)
        hdr_layout.addStretch()

        self._lbl_count = QLabel("0 lines")
        self._lbl_count.setStyleSheet(f"font-size:8px;color:{T.TEXT_MUTED};")
        hdr_layout.addWidget(self._lbl_count)

        layout.addWidget(hdr)

        # Toolbar: search + controls
        toolbar = QFrame()
        toolbar.setStyleSheet(f"background:{T.BG_INPUT};border-bottom:1px solid {T.BORDER_DEFAULT};")
        toolbar.setFixedHeight(26)
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(8, 0, 8, 0)
        tb_layout.setSpacing(6)

        lbl_filter = QLabel("FILTER:")
        lbl_filter.setStyleSheet(f"font-size:9px;color:{T.TEXT_MUTED};")
        tb_layout.addWidget(lbl_filter)

        self._filter_input = QLineEdit()
        self._filter_input.setPlaceholderText("keyword...")
        self._filter_input.setFixedWidth(140)
        self._filter_input.setStyleSheet(f"""
            QLineEdit {{
                background:{T.BG_ELEVATED};border:1px solid {T.BORDER_DEFAULT};
                color:{T.ACCENT_CYAN};font-size:10px;padding:1px 5px;
            }}
        """)
        self._filter_input.textChanged.connect(self._on_filter_changed)
        tb_layout.addWidget(self._filter_input)

        tb_layout.addStretch()

        self._chk_autoscroll = QCheckBox("AUTO-SCROLL")
        self._chk_autoscroll.setChecked(True)
        self._chk_autoscroll.setStyleSheet(f"color:{T.TEXT_MUTED};font-size:9px;")
        # FIXED: Using a standard method instead of lambda for better PyQt5 stability
        self._chk_autoscroll.toggled.connect(self._toggle_autoscroll)
        tb_layout.addWidget(self._chk_autoscroll)

        btn_clear = QPushButton("CLEAR")
        btn_clear.setFixedWidth(52)
        btn_clear.clicked.connect(self.clear_log)
        tb_layout.addWidget(btn_clear)

        btn_export = QPushButton("EXPORT")
        btn_export.setFixedWidth(58)
        btn_export.clicked.connect(self._export_log)
        tb_layout.addWidget(btn_export)

        layout.addWidget(toolbar)

        # Terminal text area
        self._text_edit = QTextEdit()
        self._text_edit.setReadOnly(True)
        # FIXED: PyQt5 syntax for NoWrap
        self._text_edit.setLineWrapMode(QTextEdit.NoWrap)
        self._text_edit.setStyleSheet(f"""
            QTextEdit {{
                background:{T.BG_PRIMARY};
                color:{T.ACCENT_CYAN_MID};
                border:none;
                font-family:{T.FONT_MONO};
                font-size:11px;
                padding:6px 10px;
            }}
        """)
        layout.addWidget(self._text_edit, 1)

        # Level legend
        legend = QFrame()
        legend.setStyleSheet(f"background:{T.BG_INPUT};border-top:1px solid {T.BORDER_DEFAULT};")
        legend.setFixedHeight(20)
        leg_layout = QHBoxLayout(legend)
        leg_layout.setContentsMargins(8, 0, 8, 0)
        leg_layout.setSpacing(12)
        for lvl, color in LEVEL_COLORS.items():
            lbl_leg = QLabel(f"■ {lvl}")
            lbl_leg.setStyleSheet(f"font-size:8px;color:{color};")
            leg_layout.addWidget(lbl_leg)
        leg_layout.addStretch()
        layout.addWidget(legend)

    # ── Public API ───────────────────────────

    @pyqtSlot(str, str)
    def append_line(self, text: str, level: str = "INFO"):
        """Thread-safe slot: add a log line."""
        ts = datetime.now().strftime("%H:%M:%S.%f")[:12]
        full_line = f"[{ts}] [{level:5}] {text}"
        self._buffer.append((ts, level.upper(), text))

        # Apply filter
        if self._filter_text and self._filter_text.lower() not in full_line.lower():
            self._lbl_count.setText(f"{len(self._buffer)} lines")
            return

        self._write_line(full_line, level.upper())
        self._lbl_count.setText(f"{len(self._buffer)} lines")

    def append_sys(self, text: str):
        self.append_line(text, "SYS")

    def clear_log(self):
        self._buffer.clear()
        self._text_edit.clear()
        self._lbl_count.setText("0 lines")

    # ── Internal ─────────────────────────────

    def _toggle_autoscroll(self, state):
        self._auto_scroll = state

    def _write_line(self, text: str, level: str):
        fmt = QTextCharFormat()
        color_hex = LEVEL_COLORS.get(level, T.ACCENT_CYAN_MID)
        fmt.setForeground(QColor(color_hex))
        # Ensure only the primary font name is passed to QFont
        font_name = T.FONT_MONO.split(",").strip()
        fmt.setFont(QFont(font_name, 9))

        cursor = self._text_edit.textCursor()
        # FIXED: PyQt5 syntax for End position
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text + "\n", fmt)

        if self._auto_scroll:
            self._text_edit.setTextCursor(cursor)
            self._text_edit.ensureCursorVisible()

    def _on_filter_changed(self, text: str):
        self._filter_text = text
        self._redraw_from_buffer()

    def _redraw_from_buffer(self):
        self._text_edit.clear()
        flt = self._filter_text.lower()
        for ts, level, text in self._buffer:
            full_line = f"[{ts}] [{level:5}] {text}"
            if flt and flt not in full_line.lower():
                continue
            self._write_line(full_line, level)

    def _export_log(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Log", "", "Log Files (*.log);;Text Files (*.txt)"
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    for ts, level, text in self._buffer:
                        f.write(f"[{ts}] [{level}] {text}\n")
                self.append_sys(f"Log exported to {path}")
            except Exception as e:
                self.append_line(f"Export failed: {e}", "ERROR")