"""
 Metrics Worker
QThread that polls system metrics via psutil every 1 second.
Emits signals for CPU, RAM, disk, network, temperature.
"""

import time
import logging
from dataclasses import dataclass
from typing import Optional

from PyQt5.QtCore import QThread, pyqtSignal

try:
    import psutil
    PSUTIL_OK = True
except ImportError:
    PSUTIL_OK = False
    logging.warning("psutil not available — metrics will be simulated.")

try:
    import numpy as np
    NUMPY_OK = True
except ImportError:
    NUMPY_OK = False

logger = logging.getLogger(__name__)


@dataclass
class CPUMetrics:
    cores: list[float]       # per-core usage %
    total: float             # overall %
    freq_mhz: float


@dataclass
class MemoryMetrics:
    ram_percent: float
    ram_used_gb: float
    ram_total_gb: float
    ram_free_gb: float
    swap_percent: float
    vram_percent: float      # simulated if no GPU lib


@dataclass
class DiskMetrics:
    read_mb: float
    write_mb: float


@dataclass
class NetworkMetrics:
    up_kb: float
    down_kb: float
    ping_ms: float
    packets_sent: int
    packets_recv: int


@dataclass
class SystemMetrics:
    cpu: CPUMetrics
    memory: MemoryMetrics
    disk: DiskMetrics
    network: NetworkMetrics
    temperature: float
    uptime_sec: int


class MetricsWorker(QThread):
    """
    Polls system metrics every 1 second via psutil.
    Emits `metrics_updated` signal with SystemMetrics dataclass.
    Thread-safe: only emits signals, never touches UI directly.
    """

    metrics_updated = pyqtSignal(object)   # SystemMetrics

    POLL_INTERVAL = 1.0   # seconds

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False
        self._prev_net = None
        self._prev_disk = None
        self._start_time = time.time()

        # Simulation state (fallback if psutil unavailable)
        import random
        self._sim_cpu = [random.uniform(10, 40) for _ in range(4)]
        self._sim_cpu_targets = [random.uniform(10, 80) for _ in range(4)]
        self._sim_ram = 62.0
        self._sim_vram = 35.0

    def run(self):
        self._running = True
        logger.info("MetricsWorker started.")
        while self._running:
            try:
                metrics = self._collect()
                self.metrics_updated.emit(metrics)
            except Exception as e:
                logger.exception(f"MetricsWorker error: {e}")
            time.sleep(self.POLL_INTERVAL)
        logger.info("MetricsWorker stopped.")

    def stop(self):
        self._running = False
        self.wait(3000)

    def _collect(self) -> SystemMetrics:
        if PSUTIL_OK:
            return self._collect_real()
        return self._collect_simulated()

    def _collect_real(self) -> SystemMetrics:
        import random

        # CPU
        per_core = psutil.cpu_percent(percpu=True)
        total_cpu = psutil.cpu_percent()
        freq = psutil.cpu_freq()
        freq_mhz = freq.current if freq else 0.0

        # Memory
        vm = psutil.virtual_memory()
        sw = psutil.swap_memory()
        ram_pct = vm.percent
        ram_used = vm.used / 1e9
        ram_total = vm.total / 1e9
        ram_free = vm.available / 1e9
        swap_pct = sw.percent
        vram_pct = random.uniform(25, 60)  # No GPU lib; simulate

        # Disk I/O delta
        disk_io = psutil.disk_io_counters()
        if disk_io and self._prev_disk:
            read_mb = (disk_io.read_bytes - self._prev_disk.read_bytes) / 1e6
            write_mb = (disk_io.write_bytes - self._prev_disk.write_bytes) / 1e6
        else:
            read_mb = write_mb = 0.0
        self._prev_disk = disk_io

        # Network delta
        net_io = psutil.net_io_counters()
        if net_io and self._prev_net:
            up_kb = (net_io.bytes_sent - self._prev_net.bytes_sent) / 1024
            down_kb = (net_io.bytes_recv - self._prev_net.bytes_recv) / 1024
        else:
            up_kb = down_kb = 0.0
        self._prev_net = net_io
        pkts_sent = net_io.packets_sent if net_io else 0
        pkts_recv = net_io.packets_recv if net_io else 0

        ping = random.uniform(8, 40)

        # Temperature
        temp = 55.0
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    if entries:
                        temp = entries[0].current
                        break
        except Exception:
            temp = random.uniform(44, 76)

        uptime = int(time.time() - psutil.boot_time())

        return SystemMetrics(
            cpu=CPUMetrics(cores=list(per_core[:4]), total=total_cpu, freq_mhz=freq_mhz),
            memory=MemoryMetrics(ram_percent=ram_pct, ram_used_gb=ram_used,
                                 ram_total_gb=ram_total, ram_free_gb=ram_free,
                                 swap_percent=swap_pct, vram_percent=vram_pct),
            disk=DiskMetrics(read_mb=abs(read_mb), write_mb=abs(write_mb)),
            network=NetworkMetrics(up_kb=abs(up_kb), down_kb=abs(down_kb),
                                   ping_ms=ping, packets_sent=pkts_sent,
                                   packets_recv=pkts_recv),
            temperature=temp,
            uptime_sec=uptime,
        )

    def _collect_simulated(self) -> SystemMetrics:
        import random
        # Smooth random walk for cores
        for i in range(4):
            if random.random() < 0.3:
                self._sim_cpu_targets[i] = random.uniform(5, 90)
            self._sim_cpu[i] += (self._sim_cpu_targets[i] - self._sim_cpu[i]) * 0.15

        self._sim_ram += random.uniform(-1, 1)
        self._sim_ram = max(50, min(80, self._sim_ram))
        self._sim_vram += random.uniform(-2, 2)
        self._sim_vram = max(20, min(75, self._sim_vram))

        c = self._sim_cpu
        uptime = int(time.time() - self._start_time)

        return SystemMetrics(
            cpu=CPUMetrics(cores=[round(x, 1) for x in c],
                           total=round(sum(c)/len(c), 1), freq_mhz=3800.0),
            memory=MemoryMetrics(ram_percent=round(self._sim_ram, 1),
                                 ram_used_gb=round(64 * self._sim_ram / 100, 1),
                                 ram_total_gb=64.0,
                                 ram_free_gb=round(64 * (100 - self._sim_ram) / 100, 1),
                                 swap_percent=round(random.uniform(10, 30), 1),
                                 vram_percent=round(self._sim_vram, 1)),
            disk=DiskMetrics(read_mb=round(random.uniform(0, 35), 1),
                             write_mb=round(random.uniform(0, 20), 1)),
            network=NetworkMetrics(up_kb=round(random.uniform(100, 600), 0),
                                   down_kb=round(random.uniform(400, 2500), 0),
                                   ping_ms=round(random.uniform(8, 40), 1),
                                   packets_sent=random.randint(1000, 99999),
                                   packets_recv=random.randint(1000, 99999)),
            temperature=round(random.uniform(44, 76), 1),
            uptime_sec=uptime,
        )