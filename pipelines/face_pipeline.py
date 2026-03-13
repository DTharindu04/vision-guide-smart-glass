from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Dict, Any, List

import cv2
import numpy as np

from config import FACE, PATHS, RULES
from camera.camera_utils import crop_safe, expand_bbox, variance_of_laplacian
from utils.image_utils import cosine_similarity

logger = logging.getLogger(__name__)


class FaceDatabase:
    def __init__(self):
        self.embeddings = np.empty((0, 128), dtype=np.float32)
        self.names: list[str] = []
        self.reload()

    def reload(self):
        emb_path = Path(PATHS['face_embeddings'])
        meta_path = Path(PATHS['face_metadata'])
        if emb_path.exists() and meta_path.exists():
            data = np.load(emb_path)
            self.embeddings = data['embeddings'].astype(np.float32)
            meta = json.loads(meta_path.read_text())
            self.names = meta['names']
            logger.info('Loaded %d face embeddings', len(self.names))

    def identify(self, emb: np.ndarray, threshold: float) -> tuple[str, float]:
        if len(self.embeddings) == 0:
            return 'unknown', 0.0
        sims = np.array([cosine_similarity(emb, db_emb) for db_emb in self.embeddings], dtype=np.float32)
        idx = int(np.argmax(sims))
        best = float(sims[idx])
        return (self.names[idx], best) if best >= threshold else ('unknown', best)


class FacePipeline:
    def __init__(self):
        self.detector = None
        self.recognizer = None
        self.db = FaceDatabase()
        self.available = False
        try:
            self.detector = cv2.FaceDetectorYN.create(FACE['detector_path'], '', FACE['input_size'], FACE['score_thres'], FACE['nms_thres'], FACE['top_k'])
            self.recognizer = cv2.FaceRecognizerSF.create(FACE['recognizer_path'], '')
            self.available = True
            logger.info('Loaded YuNet + SFace models')
        except Exception as exc:
            logger.warning('Face pipeline unavailable: %s', exc)

    def run(self, frame, rois: List[tuple] | None, frame_id: int) -> Dict[str, Any]:
        if not self.available:
            return {'frame_id': frame_id, 'faces': [], 'recognized_face': None}

        faces_out = []
        recognized = None
        target_regions = rois or [(0, 0, frame.shape[1], frame.shape[0])]

        for roi in target_regions[:RULES['max_faces_per_frame']]:
            ex_roi = expand_bbox(roi, frame.shape, 1.15)
            crop = crop_safe(frame, ex_roi)
            if crop is None:
                continue
            h, w = crop.shape[:2]
            self.detector.setInputSize((w, h))
            _, faces = self.detector.detect(crop)
            if faces is None:
                continue
            for face in faces[:RULES['max_faces_per_frame']]:
                x, y, fw, fh = face[:4].astype(int)
                if min(fw, fh) < FACE['min_face_size']:
                    continue
                full_face = face.copy()
                full_face[0] += ex_roi[0]
                full_face[1] += ex_roi[1]

                face_patch = crop_safe(frame, [int(full_face[0]), int(full_face[1]), int(full_face[0] + full_face[2]), int(full_face[1] + full_face[3])])
                if face_patch is None:
                    continue
                clarity = variance_of_laplacian(face_patch)
                if clarity < FACE['clear_face_var_thres']:
                    continue

                aligned = self.recognizer.alignCrop(frame, full_face)
                emb = self.recognizer.feature(aligned)
                name, score = self.db.identify(emb.flatten(), FACE['recognition_threshold'])
                entry = {
                    'bbox': [int(full_face[0]), int(full_face[1]), int(full_face[0] + full_face[2]), int(full_face[1] + full_face[3])],
                    'name': name,
                    'score': round(float(score), 3),
                    'clearity': round(float(clarity), 1),
                    'landmarks': face[4:14].reshape(-1, 2).astype(int).tolist() if len(face) >= 14 else [],
                }
                faces_out.append(entry)
                if recognized is None or entry['score'] > recognized['score']:
                    recognized = entry

        return {'frame_id': frame_id, 'faces': faces_out, 'recognized_face': recognized}
