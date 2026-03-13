import os
import time
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class HealthMonitor:
    def __init__(self):
        self.last = {}

    def sample(self) -> Dict[str, float]:
        cpu_temp = None
        temp_path = '/sys/class/thermal/thermal_zone0/temp'
        if os.path.exists(temp_path):
            try:
                cpu_temp = float(open(temp_path).read().strip()) / 1000.0
            except Exception:
                cpu_temp = None
        health = {
            'time': time.time(),
            'cpu_temp_c': cpu_temp if cpu_temp is not None else -1.0,
        }
        self.last = health
        return health
