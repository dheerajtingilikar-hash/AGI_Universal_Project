"""
VERONIX — Virtual Keyboard Widget
Full interactive keyboard that lights up on keypresses.
Sends key characters to a connected QLineEdit target.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QKeyEvent

# Change this from 'import gui.theme' to relative import
from . import Theme as T

# Keyboard layout definition
ROWS = [
    [("ESC","Escape",1.5),("F1","F1",1),("F2","F2",1),("F3","F3",1),("F4","F4",1),
     ("F5","F5",1),("F6","F6",1),("F7","F7",1),("F8","F8",1),
     ("F9","F9",1),("F10","F10",1),("F11","F11",1),("F12","F12",1),("DEL","Delete",1.5)],
    [("`","`",1),("1","1",1),("2","2",1),("3","3",1),("4","4",1),("5","5",1),
     ("6","6",1),("7","7",1),("8","8",1),("9","9",1),("0","0",1),
     ("-","-",1),("=","=",1),("BKSP","Backspace",1.8)],
    [("TAB","Tab",1.8),("Q","q",1),("W","w",1),("E","e",1),("R","r",1),("T","t",1),
     ("Y","y",1),("U","u",1),("I","i",1),("O","o",1),("P","p",1),
     ("[","[",1),("]","]",1),("\\","\\",1.8)],
    [("CAPS","CapsLock",2),("A","a",1),("S","s",1),("D","d",1),("F","f",1),
     ("G","g",1),("H","h",1),("J","j",1),("K","k",1),("L","l",1),
     (";",";",1),("'","'",1),("ENTER","Return",2.4)],
    [("SHIFT","ShiftL",2.5),("Z","z",1),("X","x",1),("C","c",1),("V","v",1),
     ("B","b",1),("N","n",1),("M","m",1),(",",",",1),(".",".",1),("/","/",1),
     ("SHIFT","ShiftR",2.5)],
    [("CTRL","CtrlL",1.5),("WIN","Win",1.5),("ALT","AltL",1.5),
     ("SPACE"," ",6),
     ("ALT","AltR",1.5),("CTRL","CtrlR",1.5)],
]

SPECIAL_KEYS = {
    "Backspace", "Delete", "Escape", "Return", "Tab",
    "CapsLock", "ShiftL", "ShiftR", "CtrlL", "CtrlR",
    "AltL", "AltR", "Win",
    "F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12",
}

class KeyButton(QPushButton):
    def __init__(self, label: str, key_id: str, width_factor: float = 1.0, parent=None):
        super().__init__(label, parent)
        self.key_id = key_id
        self.width_factor = width_factor
        self._flash_timer = QTimer(self)
        self._flash_timer.setSingleShot(True)
        self._flash_timer.timeout.connect(self._unflash)
        self._is_special = key_id in SPECIAL_KEYS
        self._apply_style(False)

    def _apply_style(self, lit: bool):
        if lit:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {T.ACCENT_CYAN_DIM};
                    color: {T.ACCENT_CYAN};
                    border: 1px solid {T.ACCENT_CYAN};
                    border-radius: 2px;
                    font-family: {T.FONT_MONO};
                    font-size: 9px;
                    padding: 3px 0px;
                }}
            """)
        else:
            base_bg = T.BG_ELEVATED if self._is_special else "#0a1a15"
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {base_bg};
                    color: {T.ACCENT_CYAN_MID};
                    border: 1px solid {T.BORDER_DEFAULT};
                    border-radius: 2px;
                    font-family: {T.FONT_MONO};
                    font-size: 9px;
                    padding: 3px 0px;
                }}
                QPushButton:hover {{
                    background-color: #0f2e22;
                    color: {T.ACCENT_CYAN};
                    border-color: {T.BORDER_MID};
                }}
            """)

    def flash(self):
        self._apply_style(True)
        self._flash_timer.start(140)

    def _unflash(self):
        self._apply_style(False)

class KeyboardWidget(QWidget):
    char_pressed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._target = None
        self._key_map = {}
        self._build_ui()

    def set_target(self, line_edit):
        self._target = line_edit

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 5, 6, 5)
        layout.setSpacing(2)

        for row in ROWS:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(2)
            row_layout.setContentsMargins(0, 0, 0, 0)

            for label, key_id, wf in row:
                btn = KeyButton(label, key_id, wf)
                # PyQt5 Policy usage
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                btn.setFixedHeight(26)
                btn.clicked.connect(lambda checked, k=key_id, b=btn: self._on_key(k, b))
                
                self._key_map[key_id] = btn
                if len(key_id) == 1:
                    self._key_map[key_id.lower()] = btn
                row_layout.addWidget(btn, int(wf * 10))

            layout.addLayout(row_layout)

    def _on_key(self, key_id: str, btn: KeyButton):
        btn.flash()
        if self._target is None:
            return
        if key_id == "Backspace":
            self._target.setText(self._target.text()[:-1])
        elif key_id == "Return":
            self._target.returnPressed.emit()
        elif key_id == "Tab":
            self._target.setText(self._target.text() + "  ")
        elif key_id not in SPECIAL_KEYS:
            self._target.setText(self._target.text() + key_id)
            self.char_pressed.emit(key_id)
        self._target.setFocus()

    def flash_key(self, key: str):
        btn = self._key_map.get(key) or self._key_map.get(key.lower())
        if btn:
            btn.flash()