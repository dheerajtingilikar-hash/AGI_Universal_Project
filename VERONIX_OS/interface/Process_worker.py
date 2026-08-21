"""
 Process Worker
QThread wrapper for subprocess.Popen.
Streams stdout/stderr line-by-line via Qt signals.
Supports start, stop, restart, kill.
"""

import os
import subprocess
import logging
import time
import threading
from pathlib import Path
from typing import Optional

# Converted to PyQt5
from PyQt5.QtCore import QThread, pyqtSignal

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(r"D:\AGI_Universal_Project")

class ProcessWorker(QThread):
    """
    Manages a single subprocess (AGI script).
    Emits line-by-line output and status change signals.
    Thread-safe communication via Qt signals.
    """

    # Signals
    line_received  = pyqtSignal(str, str)   # (line_text, level)
    status_changed = pyqtSignal(str, str)   # (process_name, status)
    started_ok     = pyqtSignal(str)        # process_name
    stopped        = pyqtSignal(str)        # process_name
    error_occurred = pyqtSignal(str, str)   # (process_name, error_message)

    DEGRADED_TIMEOUT = 15.0   # seconds of no output → degraded status

    def __init__(self, name: str, script_path: str,
                 args: Optional[list] = None, parent=None):
        super().__init__(parent)
        self.name = name
        self.script_path = Path(script_path)
        self.args = args or []
        self._process: Optional[subprocess.Popen] = None
        self._running = False
        self._last_output_time = time.time()

    # ── Public API ────────────────────────────────

    def start_process(self):
        """Start the subprocess and this worker thread."""
        if not self.isRunning():
            self._running = True
            self.start()

    def stop_process(self):
        """Gracefully stop subprocess."""
        self._running = False
        if self._process and self._process.poll() is None:
            try:
                self._process.terminate()
                self._process.wait(timeout=1.0)
            except:
                if self._process:
                    self._process.kill()
        self.wait(1000)

    def kill_process(self):
        """Immediately kill the subprocess."""
        self._running = False
        if self._process and self._process.poll() is None:
            try:
                self._process.kill()
            except Exception as e:
                logger.error(f"{self.name}: kill error: {e}")

    def restart_process(self):
        """Stop then restart the subprocess."""
        self.stop_process()
        time.sleep(0.2)
        self.start_process()

    @property
    def is_alive(self) -> bool:
        return self._process is not None and self._process.poll() is None

    # ── Thread run loop ────────────────────────────────

    def run(self):
        logger.info(f"ProcessWorker [{self.name}] starting: {self.script_path}")
        self.status_changed.emit(self.name, "online")

        try:
            # Construct command
            cmd = ["python", "-u", str(self.script_path)] + self.args
            
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(PROJECT_ROOT),
                env=os.environ.copy(),
                text=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            self.started_ok.emit(self.name)
            self._last_output_time = time.time()

            # Start streaming threads
            t1 = threading.Thread(target=self._stream_reader, args=(self._process.stdout, "stdout"), daemon=True)
            t2 = threading.Thread(target=self._stream_reader, args=(self._process.stderr, "stderr"), daemon=True)
            t1.start()
            t2.start()

            # Monitor loop
            while self._running and self._process.poll() is None:
                # Check for "Degraded" status (lack of activity)
                if time.time() - self._last_output_time > self.DEGRADED_TIMEOUT:
                    self.status_changed.emit(self.name, "warn")
                self.msleep(500)

            # Cleanup
            rc = self._process.wait()
            if rc != 0 and self._running:
                self.error_occurred.emit(self.name, f"exit code {rc}")

        except Exception as e:
            logger.exception(f"{self.name}: execution error: {e}")
            self.error_occurred.emit(self.name, str(e))
        finally:
            self.status_changed.emit(self.name, "offline")
            self.stopped.emit(self.name)
            self._running = False

    def _stream_reader(self, pipe, stream_type):
        """Reads lines from the subprocess pipe in a separate thread."""
        try:
            with pipe:
                for line in iter(pipe.readline, ''):
                    if not line: break
                    clean_line = line.rstrip()
                    if clean_line:
                        self._emit_line(clean_line, stream_type)
                        self._last_output_time = time.time()
                        # Re-assert online if we were warned/degraded
                        self.status_changed.emit(self.name, "online")
        except Exception as e:
            logger.debug(f"Stream reader error for {self.name}: {e}")

    def _emit_line(self, line: str, stream: str):
        """Classify log level and emit signal."""
        level = "INFO"
        low = line.lower()
        if any(x in low for x in ["error", "exception", "traceback", "failed"]):
            level = "ERROR"
        elif any(x in low for x in ["warning", "warn", "degraded"]):
            level = "WARN"
        elif "debug" in low:
            level = "DEBUG"
        elif stream == "stderr":
            level = "ERROR"
        
        self.line_received.emit(line, level)