"""
VERONIX / OMNI-BRAIN — Theme System
All color constants and QSS stylesheet.
"""

# ── Color Palette ─────────────────────────────────────────────────────────────
BG_PRIMARY      = "#070d0d"
BG_SURFACE      = "#050d0b"
BG_ELEVATED     = "#0a1a15"
BG_INPUT        = "#040c0a"

ACCENT_CYAN     = "#00ffcc"
ACCENT_CYAN_DIM = "#00ffcc44"
ACCENT_CYAN_MID = "#00ffcc88"

COLOR_ONLINE    = "#00ff88"
COLOR_WARN      = "#ffaa00"
COLOR_DANGER    = "#ff3b3b"
COLOR_IDLE      = "#555555"

BORDER_DEFAULT  = "#00ffcc22"
BORDER_MID      = "#00ffcc44"
BORDER_STRONG   = "#00ffcc88"

TEXT_PRIMARY    = "#e8e8e8"
TEXT_SECONDARY  = "#00ffcc88"
TEXT_MUTED      = "#00ffcc44"
TEXT_INFO       = "#ffaa00"
TEXT_OK         = "#00ff88"
TEXT_ERR        = "#ff3b3b"

FONT_MONO       = "JetBrains Mono, Consolas, Courier New, monospace"


def get_stylesheet() -> str:
    """Return the full QSS stylesheet for the application."""
    return f"""
/* ── Global ─────────────────────────────────────────────── */
QMainWindow, QWidget {{
    background-color: {BG_PRIMARY};
    color: {ACCENT_CYAN};
    font-family: {FONT_MONO};
    font-size: 11px;
}}

QSplitter::handle {{
    background-color: {BORDER_DEFAULT};
    width: 1px;
    height: 1px;
}}

/* ── Scroll Bars ─────────────────────────────────────────── */
QScrollBar:vertical {{
    background: {BG_PRIMARY};
    width: 6px;
    border: none;
}}
QScrollBar::handle:vertical {{
    background: {ACCENT_CYAN_DIM};
    border-radius: 3px;
    min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{
    background: {ACCENT_CYAN_MID};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar:horizontal {{
    background: {BG_PRIMARY};
    height: 6px;
    border: none;
}}
QScrollBar::handle:horizontal {{
    background: {ACCENT_CYAN_DIM};
    border-radius: 3px;
    min-width: 20px;
}}

/* ── QTextEdit (Terminal / Log) ──────────────────────────── */
QTextEdit {{
    background-color: {BG_PRIMARY};
    color: {ACCENT_CYAN_MID};
    border: none;
    font-family: {FONT_MONO};
    font-size: 11px;
    selection-background-color: {ACCENT_CYAN_DIM};
}}

/* ── QLineEdit (Input) ───────────────────────────────────── */
QLineEdit {{
    background-color: transparent;
    color: {ACCENT_CYAN};
    border: none;
    font-family: {FONT_MONO};
    font-size: 11px;
    padding: 0px;
}}
QLineEdit:focus {{
    border-bottom: 1px solid {ACCENT_CYAN_DIM};
}}

/* ── QPushButton ─────────────────────────────────────────── */
QPushButton {{
    background-color: {BG_ELEVATED};
    color: {ACCENT_CYAN_MID};
    border: 1px solid {BORDER_DEFAULT};
    border-radius: 2px;
    padding: 3px 8px;
    font-family: {FONT_MONO};
    font-size: 9px;
}}
QPushButton:hover {{
    background-color: {BG_ELEVATED};
    color: {ACCENT_CYAN};
    border-color: {BORDER_MID};
}}
QPushButton:pressed {{
    background-color: {ACCENT_CYAN_DIM};
    color: {ACCENT_CYAN};
}}
QPushButton#btn-danger {{
    color: {COLOR_DANGER};
    border-color: {COLOR_DANGER}44;
}}
QPushButton#btn-danger:hover {{
    background-color: {COLOR_DANGER}22;
    border-color: {COLOR_DANGER};
}}
QPushButton#btn-warn {{
    color: {COLOR_WARN};
    border-color: {COLOR_WARN}44;
}}
QPushButton#btn-warn:hover {{
    background-color: {COLOR_WARN}22;
    border-color: {COLOR_WARN};
}}

/* ── QLabel ─────────────────────────────────────────────── */
QLabel {{
    background: transparent;
    color: {ACCENT_CYAN_MID};
    font-family: {FONT_MONO};
    font-size: 9px;
}}
QLabel#section-title {{
    color: {TEXT_MUTED};
    font-size: 9px;
    letter-spacing: 2px;
    border-bottom: 1px solid {BORDER_DEFAULT};
    padding-bottom: 3px;
}}
QLabel#value-label {{
    color: {ACCENT_CYAN};
    font-size: 9px;
}}
QLabel#status-online  {{ color: {COLOR_ONLINE}; font-size: 8px; font-weight: bold; }}
QLabel#status-offline {{ color: {COLOR_DANGER}; font-size: 8px; font-weight: bold; }}
QLabel#status-warn    {{ color: {COLOR_WARN};   font-size: 8px; font-weight: bold; }}

/* ── QProgressBar ────────────────────────────────────────── */
QProgressBar {{
    background-color: #001a13;
    border: 1px solid {BORDER_DEFAULT};
    border-radius: 0px;
    height: 5px;
    text-align: center;
    color: transparent;
}}
QProgressBar::chunk {{
    background-color: {ACCENT_CYAN};
    border-radius: 0px;
}}
QProgressBar#bar-warn::chunk  {{ background-color: {COLOR_WARN}; }}
QProgressBar#bar-danger::chunk {{ background-color: {COLOR_DANGER}; }}

/* ── QTreeView (Knowledge Base) ──────────────────────────── */
QTreeView {{
    background-color: {BG_SURFACE};
    color: {ACCENT_CYAN_MID};
    border: 1px solid {BORDER_DEFAULT};
    font-size: 10px;
    alternate-background-color: {BG_ELEVATED};
}}
QTreeView::item:hover {{
    background-color: {ACCENT_CYAN_DIM};
}}
QTreeView::item:selected {{
    background-color: {ACCENT_CYAN_DIM};
    color: {ACCENT_CYAN};
}}
QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {{
    color: {ACCENT_CYAN_MID};
}}

/* ── QDockWidget ─────────────────────────────────────────── */
QDockWidget {{
    titlebar-close-icon: none;
    titlebar-normal-icon: none;
    color: {ACCENT_CYAN};
    font-size: 9px;
    letter-spacing: 2px;
}}
QDockWidget::title {{
    background-color: {BG_INPUT};
    border-bottom: 1px solid {BORDER_DEFAULT};
    padding: 4px 8px;
    text-align: left;
}}

/* ── QTabWidget ──────────────────────────────────────────── */
QTabWidget::pane {{
    border: 1px solid {BORDER_DEFAULT};
    background-color: {BG_PRIMARY};
}}
QTabBar::tab {{
    background-color: {BG_SURFACE};
    color: {TEXT_MUTED};
    border: 1px solid {BORDER_DEFAULT};
    padding: 4px 14px;
    font-size: 9px;
    letter-spacing: 1px;
}}
QTabBar::tab:selected {{
    background-color: {BG_ELEVATED};
    color: {ACCENT_CYAN};
    border-bottom: 1px solid {ACCENT_CYAN};
}}
QTabBar::tab:hover {{
    color: {ACCENT_CYAN_MID};
}}

/* ── QFrame (panels) ─────────────────────────────────────── */
QFrame#panel-frame {{
    background-color: {BG_SURFACE};
    border: 1px solid {BORDER_DEFAULT};
}}
QFrame#top-bar {{
    background-color: {BG_INPUT};
    border-bottom: 1px solid {BORDER_MID};
}}
QFrame#input-bar {{
    background-color: {BG_INPUT};
    border-top: 1px solid {BORDER_DEFAULT};
}}
"""
