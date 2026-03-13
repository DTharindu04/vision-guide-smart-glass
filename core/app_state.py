from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Dict, Optional
import time


@dataclass
class RuntimeStats:
    frame_id: int = 0
    object_runs: int = 0
    face_runs: int = 0
    emotion_runs: int = 0
    ocr_runs: int = 0
    dropped_audio: int = 0
    avg_loop_ms: float = 0.0


@dataclass
class AppState:
    running: bool = True
    mode: str = 'navigation'
    reading_mode: bool = False
    low_light: bool = False
    blurry: bool = False
    last_frame_ts: float = 0.0
    last_object_result: Optional[Dict[str, Any]] = None
    last_face_result: Optional[Dict[str, Any]] = None
    last_ocr_text: str = ''
    last_health: Dict[str, Any] = field(default_factory=dict)
    stats: RuntimeStats = field(default_factory=RuntimeStats)
    _lock: Lock = field(default_factory=Lock)

    def update(self, **kwargs):
        with self._lock:
            for k, v in kwargs.items():
                setattr(self, k, v)

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {
                'running': self.running,
                'mode': self.mode,
                'reading_mode': self.reading_mode,
                'low_light': self.low_light,
                'blurry': self.blurry,
                'last_frame_ts': self.last_frame_ts,
                'last_object_result': self.last_object_result,
                'last_face_result': self.last_face_result,
                'last_ocr_text': self.last_ocr_text,
                'last_health': dict(self.last_health),
                'stats': self.stats.__dict__.copy(),
                'time': time.time(),
            }
