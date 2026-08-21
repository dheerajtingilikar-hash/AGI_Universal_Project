"""
VERONIX / OMNI-BRAIN — GUI Theme (PyQt5)
"""

BG_PRIMARY    = "#070d0d"
BG_SURFACE    = "#050d0b"
BG_ELEVATED   = "#0a1a15"
BG_INPUT      = "#040c0a"
BORDER        = "#1a3a2a"
BORDER_ACCENT = "#00ffcc55"
ACCENT_CYAN   = "#00ffcc"
ACCENT_GREEN  = "#00ff88"
ACCENT_AMBER  = "#ffaa00"
ACCENT_RED    = "#ff3b3b"
TEXT_PRIMARY  = "#d0fff5"
TEXT_SECONDARY= "#00ffcc99"
TEXT_MUTED    = "#00ffcc44"

QSS = """
* {
    font-family: 'Courier New', Consolas, monospace;
    font-size: 11px;
}
QMainWindow, QWidget {
    background-color: #070d0d;
    color: #d0fff5;
}
QTextEdit, QPlainTextEdit {
    background-color: #070d0d;
    color: #00ffcc99;
    border: none;
    selection-background-color: #0a1a15;
}
QLineEdit {
    background-color: #040c0a;
    color: #00ffcc;
    border: 1px solid #1a3a2a;
    border-radius: 2px;
    padding: 3px 6px;
}
QLineEdit:focus { border-color: #00ffcc55; }
QScrollBar:vertical {
    background: #070d0d; width: 5px; border: none;
}
QScrollBar::handle:vertical {
    background: #00ffcc44; border-radius: 2px; min-height: 16px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: #070d0d; height: 5px; border: none; }
QScrollBar::handle:horizontal { background: #00ffcc44; border-radius: 2px; }
QPushButton {
    background-color: #0a1a15;
    color: #00ffcc;
    border: 1px solid #1a3a2a;
    border-radius: 2px;
    padding: 4px 10px;
    letter-spacing: 1px;
}
QPushButton:hover { background-color: #0f2e22; border-color: #00ffcc55; }
QPushButton:pressed { background-color: #00ffcc1a; }
QPushButton#btn_screener {
    color: #00ffcc;
    border: 1px solid #00ffcc55;
    background: #001a13;
    font-weight: bold;
    letter-spacing: 2px;
}
QPushButton#btn_screener:hover {
    background: #00ffcc22;
    border-color: #00ffcc;
}
QPushButton#btn_back {
    color: #00ffcc99;
    border: 1px solid #1a3a2a;
    background: #050d0b;
    letter-spacing: 2px;
}
QPushButton#btn_back:hover { background: #0f2e22; color: #00ffcc; }
QPushButton#btn_danger { color: #ff3b3b; border-color: #ff3b3b33; }
QPushButton#btn_danger:hover { background-color: #2a0808; border-color: #ff3b3b; }
QPushButton#btn_warn   { color: #ffaa00; border-color: #ffaa0033; }
QPushButton#btn_warn:hover { background-color: #2a1e00; border-color: #ffaa00; }
QProgressBar {
    background-color: #001a13;
    border: 1px solid #1a3a2a;
    border-radius: 0px;
    color: transparent;
    max-height: 5px;
}
QProgressBar::chunk        { background-color: #00ffcc; }
QProgressBar#warn::chunk   { background-color: #ffaa00; }
QProgressBar#hot::chunk    { background-color: #ff3b3b; }
QLabel { color: #00ffcc99; background: transparent; }
QLabel#accent { color: #00ffcc; }
QLabel#muted  { color: #00ffcc44; font-size: 9px; letter-spacing: 1px; }
QLabel#ok     { color: #00ff88; }
QLabel#warn   { color: #ffaa00; }
QLabel#err    { color: #ff3b3b; }
QFrame#panel  { background-color: #050d0b; border: 1px solid #1a3a2a; }
QSplitter::handle { background: #1a3a2a; width: 1px; height: 1px; }
QStatusBar {
    background: #050d0b; color: #00ffcc44;
    border-top: 1px solid #1a3a2a; font-size: 10px;
}
QToolTip {
    background-color: #0a1a15; color: #00ffcc;
    border: 1px solid #00ffcc55; padding: 3px 6px;
}
"""


def apply_theme(app):
    app.setStyleSheet(QSS)