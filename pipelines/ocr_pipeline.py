from __future__ import annotations
import logging
import cv2
import pytesseract

from config import OCR

logger = logging.getLogger(__name__)


class OCRPipeline:
    def __init__(self):
        self.available = True

    def run(self, frame, frame_id: int):
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.bilateralFilter(gray, 7, 50, 50)
            gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11)
            text = pytesseract.image_to_string(gray, config=f'--oem 1 --psm {OCR["psm"]}', lang=OCR['language']).strip()
            if not text:
                return None
            text = ' '.join(text.split())[: OCR['max_chars_spoken']]
            return {'frame_id': frame_id, 'text': text}
        except Exception as exc:
            logger.warning('OCR failed: %s', exc)
            return None
