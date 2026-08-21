"""
VERONIX — Metrics Worker (PyQt5)
Polls CPU, RAM, disk, network via psutil every second.
Emits a single dict signal so all panels share one thread.
"""
import time
import psutil

from PyQt5.QtCore import QThread, pyqtSignal


class MetricsWorker(QThread):
    """
    Emits metrics_updated(dict) every ~1 second.

    Dict keys:
        cpu_cores   : list[float]   per-core %
        cpu_total   : float
        ram_pct     : float
        ram_used_gb : float
        ram_free_gb : float
        swap_pct    : float
        disk_read   : float  MB/s
        disk_write  : float  MB/s
        net_sent    : float  KB/s
        net_recv    : float  KB/s
        temp        : float  °C (0 if unavailable)
    """

    metrics_updated = pyqtSignal(dict)

    def __init__(self, parent=None, interval: float = 1.0):
        super().__init__(parent)
        self._interval = interval
        self._running  = False

    def stop(self):
        self._running = False

    def run(self):
        self._running = True
        prev_disk = psutil.disk_io_counters()
        prev_net  = psutil.net_io_counters()
        prev_time = time.monotonic()

        while self._running:
            time.sleep(self._interval)
            now = time.monotonic()
            dt  = max(now - prev_time, 0.001)
            prev_time = now

            # CPU
            cores = psutil.cpu_percent(percpu=True)
            total = psutil.cpu_percent()

            # RAM
            mem       = psutil.virtual_memory()
            swap      = psutil.swap_memory()
            ram_pct   = mem.percent
            ram_used  = mem.used  / 1024**3
            ram_free  = mem.available / 1024**3
            swap_pct  = swap.percent

            # Disk I/O
            disk = psutil.disk_io_counters()
            dr   = (disk.read_bytes  - prev_disk.read_bytes)  / dt / 1024**2
            dw   = (disk.write_bytes - prev_disk.write_bytes) / dt / 1024**2
            prev_disk = disk

            # Network
            net  = psutil.net_io_counters()
            ns   = (net.bytes_sent - prev_net.bytes_sent) / dt / 1024
            nr   = (net.bytes_recv - prev_net.bytes_recv) / dt / 1024
            prev_net = net

            # Temperature
            temp = 0.0
            try:
                temps = psutil.sensors_temperatures()
                for key in ("coretemp", "k10temp", "cpu_thermal"):
                    if key in temps and temps[key]:
                        temp = temps[key][0].current
                        break
            except Exception:
                pass

            self.metrics_updated.emit({
                "cpu_cores":   cores,
                "cpu_total":   total,
                "ram_pct":     ram_pct,
                "ram_used_gb": ram_used,
                "ram_free_gb": ram_free,
                "swap_pct":    swap_pct,
                "disk_read":   max(0.0, dr),
                "disk_write":  max(0.0, dw),
                "net_sent":    max(0.0, ns),
                "net_recv":    max(0.0, nr),
                "temp":        temp,
            })