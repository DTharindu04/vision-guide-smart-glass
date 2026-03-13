from __future__ import annotations
from dataclasses import dataclass, field
from queue import PriorityQueue, Full, Empty
from typing import Any
import time
import threading
import logging

from config import AUDIO

logger = logging.getLogger(__name__)


@dataclass(order=True)
class AudioMessage:
    priority: int
    timestamp: float
    text: str = field(compare=False)
    key: str = field(compare=False, default='')
    interrupt: bool = field(compare=False, default=False)
    meta: Any = field(compare=False, default=None)


class AudioQueue:
    def __init__(self, tts_engine, app_state=None):
        self.tts = tts_engine
        self.q = PriorityQueue(maxsize=AUDIO['queue_maxsize'])
        self.last_spoken = {}
        self.running = False
        self.thread: threading.Thread | None = None
        self.app_state = app_state

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._loop, name='audio_queue', daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)

    def push(self, text: str, priority: int, key: str, interrupt: bool = False):
        now = time.time()
        if key and (now - self.last_spoken.get(key, 0)) < AUDIO['dedupe_window_sec']:
            return False
        try:
            self.q.put_nowait(AudioMessage(priority=priority, timestamp=now, text=text, key=key, interrupt=interrupt))
            return True
        except Full:
            logger.warning('Audio queue full; dropped: %s', text)
            if self.app_state:
                self.app_state.stats.dropped_audio += 1
            return False

    def _loop(self):
        while self.running:
            try:
                msg: AudioMessage = self.q.get(timeout=0.2)
            except Empty:
                continue
            try:
                self.tts.speak(msg.text)
                if msg.key:
                    self.last_spoken[msg.key] = time.time()
            except Exception as exc:
                logger.warning('TTS failure: %s', exc)
