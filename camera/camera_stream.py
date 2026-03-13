from __future__ import annotations
from threading import Thread, Lock
import time
import logging
import numpy as np
import cv2

from config import CAMERA

logger = logging.getLogger(__name__)

try:
    from picamera2 import Picamera2
    PICAMERA2_AVAILABLE = True
except Exception:
    Picamera2 = None
    PICAMERA2_AVAILABLE = False


class CameraStream:
    def __init__(self):
        self.picam2 = None
        self.frame = None
        self.lock = Lock()
        self.running = False
        self.thread: Thread | None = None
        self.empty_count = 0

    def start(self):
        if self.running:
            return self
        if PICAMERA2_AVAILABLE:
            self.picam2 = Picamera2()
            config = self.picam2.create_video_configuration(
                main={'size': CAMERA['main_size'], 'format': 'RGB888'},
                lores={'size': CAMERA['lores_size'], 'format': 'YUV420'},
                controls={'FrameRate': CAMERA['fps']},
                buffer_count=CAMERA['buffer_size'],
            )
            self.picam2.configure(config)
            self.picam2.start()
            time.sleep(1.0)
        else:
            logger.warning('Picamera2 unavailable; falling back to cv2.VideoCapture(0)')
            self.picam2 = cv2.VideoCapture(0)
            self.picam2.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA['main_size'][0])
            self.picam2.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA['main_size'][1])
            self.picam2.set(cv2.CAP_PROP_FPS, CAMERA['fps'])

        self.running = True
        self.thread = Thread(target=self._reader, name='camera_reader', daemon=True)
        self.thread.start()
        return self

    def _reader(self):
        while self.running:
            try:
                if PICAMERA2_AVAILABLE:
                    arr = self.picam2.capture_array('main')
                    frame = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
                else:
                    ok, frame = self.picam2.read()
                    if not ok:
                        frame = None

                if frame is None or frame.size == 0:
                    self.empty_count += 1
                    time.sleep(CAMERA['empty_frame_sleep'])
                    continue

                if CAMERA['flip']:
                    frame = cv2.flip(frame, -1)

                with self.lock:
                    self.frame = frame
            except Exception as exc:
                logger.exception('Camera read error: %s', exc)
                time.sleep(0.2)

    def read(self):
        with self.lock:
            return None if self.frame is None else self.frame.copy()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        if self.picam2 is not None:
            try:
                if PICAMERA2_AVAILABLE:
                    self.picam2.stop()
                else:
                    self.picam2.release()
            except Exception:
                pass
