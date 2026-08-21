"""
VERONIX — Entry Point (PyQt5)
Run:  python main.py
      (from inside gui/ folder or project root)
"""
import sys
import os

# ensure project root is on path
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from gui.theme      import apply_theme
from gui.app_window import MainWindow


def main():
    # HiDPI support
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps,    True)

    app = QApplication(sys.argv)
    app.setApplicationName("VERONIX")
    app.setOrganizationName("OMNI-BRAIN")

    apply_theme(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()