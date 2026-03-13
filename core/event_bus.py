from collections import defaultdict
from queue import Queue, Empty
from threading import Thread
from typing import Callable, Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class EventBus:
    def __init__(self, maxsize: int = 256):
        self.queue: Queue = Queue(maxsize=maxsize)
        self.handlers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = defaultdict(list)
        self._running = False
        self._thread: Thread | None = None

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], None]):
        self.handlers[event_type].append(handler)

    def publish(self, event_type: str, payload: Dict[str, Any]):
        try:
            self.queue.put_nowait({'type': event_type, 'payload': payload})
        except Exception as exc:
            logger.warning('Event drop for %s: %s', event_type, exc)

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = Thread(target=self._loop, name='event_bus', daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)

    def _loop(self):
        while self._running:
            try:
                item = self.queue.get(timeout=0.2)
            except Empty:
                continue
            event_type = item['type']
            for handler in self.handlers.get(event_type, []):
                try:
                    handler(item['payload'])
                except Exception:
                    logger.exception('Event handler failed for %s', event_type)
