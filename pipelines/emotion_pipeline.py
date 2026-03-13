from __future__ import annotations
import logging
import cv2
import numpy as np

from config import EMOTION
from camera.camera_utils import crop_safe

logger = logging.getLogger(__name__)


class EmotionPipeline:
    def __init__(self):
        self.net = None
        self.available = False
        try:
            self.net = cv2.dnn.readNet(EMOTION['model_path'])
            self.available = True
            logger.info('Loaded emotion model: %s', EMOTION['model_path'])
        except Exception as exc:
            logger.warning('Emotion model unavailable: %s', exc)

    def run(self, frame, face_result, frame_id: int):
        if not self.available or not face_result:
            return None
        face = face_result.get('recognized_face')
        if not face:
            return None
        patch = crop_safe(frame, face['bbox'])
        if patch is None:
            return None
        gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, EMOTION['input_size'])
        blob = cv2.dnn.blobFromImage(gray, scalefactor=1/255.0, size=EMOTION['input_size'])
        self.net.setInput(blob)
        out = self.net.forward().flatten()
        probs = np.exp(out - np.max(out))
        probs = probs / probs.sum()
        idx = int(np.argmax(probs))
        conf = float(probs[idx])
        if conf < EMOTION['conf_thres']:
            return None
        return {
            'frame_id': frame_id,
            'name': face['name'],
            'emotion': EMOTION['labels'][idx],
            'confidence': round(conf, 3),
            'bbox': face['bbox'],
        }
