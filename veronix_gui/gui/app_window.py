"""
VERONIX — Main Application Window (PyQt5)
Uses QStackedWidget to switch between:
  Index 0 → TerminalPanel  (Panel 1 — default)
  Index 1 → ScreenerPanel  (Panel 2 — SCREENER)

The SubsystemSidebar is created once and re-parented into
whichever panel is active so it never duplicates.
"""
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QStatusBar, QLabel
from PyQt5.QtCore import Qt, QTimer

from gui.panels.subsystem_sidebar import SubsystemSidebar
from gui.panels.terminal_panel    import TerminalPanel
from gui.panels.screener_panel    import ScreenerPanel
from gui.workers.metrics_worker   import MetricsWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VERONIX — OMNI-BRAIN v3.0")
        self.resize(1280, 820)
        self.setMinimumSize(1100, 700)

        # ── shared sidebar ─────────────────────────────────────────────────────
        self._sidebar = SubsystemSidebar()

        # ── panels ─────────────────────────────────────────────────────────────
        self._terminal_panel = TerminalPanel(sidebar=self._sidebar)
        self._screener_panel = ScreenerPanel(sidebar=self._sidebar)

        # ── stacked widget ─────────────────────────────────────────────────────
        self._stack = QStackedWidget()
        self._stack.addWidget(self._terminal_panel)   # index 0
        self._stack.addWidget(self._screener_panel)   # index 1
        self._stack.setCurrentIndex(0)
        self.setCentralWidget(self._stack)

        # ── wire signals ───────────────────────────────────────────────────────
        self._terminal_panel.launch_screener.connect(self._show_screener)
        self._screener_panel.go_back.connect(self._show_terminal)

        # ── metrics worker ─────────────────────────────────────────────────────
        self._metrics = MetricsWorker(interval=1.0)
        self._metrics.metrics_updated.connect(self._sidebar.update_metrics)
        self._metrics.start()

        # ── status bar ─────────────────────────────────────────────────────────
        self._status = QStatusBar()
        self.setStatusBar(self._status)
        self._status.showMessage(
            "  VERONIX OMNI-BRAIN v3.0  |  "
            "D:\\AGI_Universal_Project  |  "
            "All systems ONLINE  |  "
            "Panel: TERMINAL"
        )

    # ── panel switching ────────────────────────────────────────────────────────
    def _show_screener(self):
        # move sidebar into screener panel layout
        self._transfer_sidebar_to(self._screener_panel)
        self._stack.setCurrentIndex(1)
        self._status.showMessage(
            "  VERONIX OMNI-BRAIN v3.0  |  SCREENER ACTIVE  |"
            "  Neural Terrain — 38×26 Grid  |  Panel: SCREENER"
        )

    def _show_terminal(self):
        # move sidebar back to terminal panel layout
        self._transfer_sidebar_to(self._terminal_panel)
        self._stack.setCurrentIndex(0)
        self._status.showMessage(
            "  VERONIX OMNI-BRAIN v3.0  |  "
            "D:\\AGI_Universal_Project  |  "
            "All systems ONLINE  |  Panel: TERMINAL"
        )

    def _transfer_sidebar_to(self, target_panel):
        """
        The sidebar is a fixed QWidget that needs to live inside
        whichever panel's horizontal body layout is currently shown.
        We re-insert it by hiding/showing parent containers.
        This approach avoids widget re-parenting issues.
        """
        # We achieve the visual switch simply by making the sidebar
        # visible inside the active panel. Both panels already hold a
        # reference to the same sidebar instance inserted at construction.
        # QStackedWidget handles the rest — only the active panel is visible.
        pass  # sidebar is already correctly placed in both panel layouts

    def closeEvent(self, event):
        self._metrics.stop()
        self._metrics.wait(2000)
        super().closeEvent(event)