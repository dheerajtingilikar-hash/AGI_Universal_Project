"""
VERONIX — Process Worker (PyQt5)
Launches a Python script as subprocess, streams lines via signal.
"""
import subprocess
from pathlib import Path

from PyQt5.QtCore import QThread, pyqtSignal

ROOT = Path(r"D:\AGI_Universal_Project")


class ProcessWorker(QThread):
    line_received   = pyqtSignal(str, str)   # (line, level)
    process_started = pyqtSignal()
    process_stopped = pyqtSignal(int)
    process_error   = pyqtSignal(str)

    def __init__(self, script_path: str, args: list = None, parent=None):
        super().__init__(parent)
        self._script  = Path(script_path)
        self._args    = args or []
        self._proc    = None
        self._running = False

    def stop(self):
        self._running = False
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self._proc.kill()

    def kill_now(self):
        self._running = False
        if self._proc and self._proc.poll() is None:
            self._proc.kill()

    def is_alive(self) -> bool:
        return self._proc is not None and self._proc.poll() is None

    def run(self):
        self._running = True
        cmd = ["python", str(self._script)] + self._args
        try:
            self._proc = subprocess.Popen(
                cmd,
                cwd=str(ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
            )
        except Exception as exc:
            self.process_error.emit(str(exc))
            return

        self.process_started.emit()
        for raw in self._proc.stdout:
            if not self._running:
                break
            line  = raw.rstrip("\n")
            level = self._classify(line)
            self.line_received.emit(line, level)

        self._proc.wait()
        code = self._proc.returncode
        self.process_stopped.emit(code if code is not None else -1)

    @staticmethod
    def _classify(line: str) -> str:
        u = line.upper()
        if any(k in u for k in ("[ERROR]", "ERROR", "EXCEPTION", "TRACEBACK")):
            return "ERROR"
        if any(k in u for k in ("[WARNING]", "WARN")):
            return "WARNING"
        if "[DEBUG]" in u or "DEBUG" in u:
            return "DEBUG"
        return "INFO"