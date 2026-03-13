from __future__ import annotations
import logging
import cv2
import numpy as np
from typing import Dict, Any, List

from config import OBJECT, CLASS_NAMES
from utils.image_utils import resize_letterbox

logger = logging.getLogger(__name__)


class ObjectPipeline:
    def __init__(self):
        self.net = None
        self.available = False
        try:
            self.net = cv2.dnn.readNet(OBJECT['model_path'])
            self.available = True
            logger.info('Loaded object model: %s', OBJECT['model_path'])
        except Exception as exc:
            logger.warning('Object model unavailable: %s', exc)

    def run(self, frame, frame_id: int) -> Dict[str, Any]:
        if not self.available:
            return {'frame_id': frame_id, 'detections': []}
        inp, scale, pad = resize_letterbox(frame, (OBJECT['input_size'], OBJECT['input_size']))
        blob = cv2.dnn.blobFromImage(inp, 1 / 255.0, (OBJECT['input_size'], OBJECT['input_size']), swapRB=True, crop=False)
        self.net.setInput(blob)
        preds = self.net.forward()
        detections = self._postprocess(preds, frame.shape, scale, pad)
        return {'frame_id': frame_id, 'detections': detections}

    def _postprocess(self, preds, original_shape, scale, pad) -> List[Dict[str, Any]]:
        preds = np.squeeze(preds)
        if preds.ndim == 1:
            preds = preds[None, :]
        boxes, scores, class_ids = [], [], []
        for row in preds:
            if row.shape[0] < 6:
                continue
            cls_scores = row[4:]
            cls_id = int(np.argmax(cls_scores))
            conf = float(cls_scores[cls_id])
            if conf < OBJECT['conf_thres']:
                continue
            x, y, w, h = row[:4]
            x1 = (x - w / 2 - pad[0]) / scale
            y1 = (y - h / 2 - pad[1]) / scale
            x2 = (x + w / 2 - pad[0]) / scale
            y2 = (y + h / 2 - pad[1]) / scale
            boxes.append([int(x1), int(y1), int(x2 - x1), int(y2 - y1)])
            scores.append(conf)
            class_ids.append(cls_id)

        indices = cv2.dnn.NMSBoxes(boxes, scores, OBJECT['conf_thres'], OBJECT['nms_thres'])
        results = []
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                x2 = x + w
                y2 = y + h
                label = CLASS_NAMES[class_ids[i]] if class_ids[i] < len(CLASS_NAMES) else str(class_ids[i])
                results.append({
                    'label': label,
                    'confidence': round(scores[i], 3),
                    'bbox': [x, y, x2, y2],
                    'area_ratio': round((w * h) / float(original_shape[0] * original_shape[1]), 4),
                })
        return results
