from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List
import logging
import numpy as np
import cv2

from config import OBJECT, FACE, OCR, RULES

logger = logging.getLogger(__name__)


@dataclass
class DecisionPlan:
    run_object: bool = True
    run_face: bool = False
    run_emotion: bool = False
    run_ocr: bool = False
    face_rois: List[tuple] | None = None
    reason: str = ''
    brightness: float = 0.0
    blur_score: float = 0.0


class DecisionEngine:
    def __init__(self):
        self.person_seen_recently = False

    @staticmethod
    def frame_quality(frame: np.ndarray) -> Dict[str, float]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = float(gray.mean())
        blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        return {'brightness': brightness, 'blur_score': blur_score}

    def plan(self, frame_id: int, frame: np.ndarray, state: Dict[str, Any]) -> DecisionPlan:
        q = self.frame_quality(frame)
        low_light = q['brightness'] < RULES['low_light_brightness_thres']
        blurry = q['blur_score'] < RULES['blurry_var_thres']

        plan = DecisionPlan(
            run_object=(frame_id % OBJECT['run_every_n_frames'] == 0),
            brightness=q['brightness'],
            blur_score=q['blur_score'],
            reason='object-primary',
        )

        last_obj = state.get('last_object_result') or {}
        persons = [d for d in last_obj.get('detections', []) if d['label'] in OBJECT['person_class_names']]
        if persons and not blurry:
            plan.run_face = True
            plan.face_rois = [tuple(p['bbox']) for p in persons[:3]]
            plan.reason += '|person->face'

        if state.get('reading_mode') and not blurry:
            plan.run_ocr = True
            plan.reason += '|reading_mode'
        elif self._frame_looks_textlike(frame) and not low_light and not blurry:
            plan.run_ocr = True
            plan.reason += '|textlike'

        face_result = state.get('last_face_result') or {}
        if face_result.get('recognized_face') and not blurry:
            plan.run_emotion = True
            plan.reason += '|recognized->emotion'

        return plan

    @staticmethod
    def _frame_looks_textlike(frame: np.ndarray) -> bool:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 80, 160)
        horizontal = cv2.reduce(edges, 1, cv2.REDUCE_AVG).reshape(-1)
        dense_rows = int((horizontal > 25).sum())
        return dense_rows > frame.shape[0] * 0.15
