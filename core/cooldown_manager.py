import time
from collections import defaultdict


class CooldownManager:
    def __init__(self):
        self.last_times = defaultdict(float)

    def ready(self, key: str, cooldown_sec: float) -> bool:
        now = time.time()
        return (now - self.last_times[key]) >= cooldown_sec

    def hit(self, key: str):
        self.last_times[key] = time.time()

    def ready_and_hit(self, key: str, cooldown_sec: float) -> bool:
        if self.ready(key, cooldown_sec):
            self.hit(key)
            return True
        return False
