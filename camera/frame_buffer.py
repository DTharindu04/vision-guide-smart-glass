from collections import deque
from threading import Lock


class FrameBuffer:
    def __init__(self, maxlen: int = 4):
        self.buffer = deque(maxlen=maxlen)
        self.lock = Lock()

    def push(self, frame):
        with self.lock:
            self.buffer.append(frame)

    def latest(self):
        with self.lock:
            return None if not self.buffer else self.buffer[-1]
