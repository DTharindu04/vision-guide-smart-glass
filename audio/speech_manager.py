from __future__ import annotations
import logging

from config import PRIORITY, RULES, FACE, OCR, EMOTION, OBJECT
from core.cooldown_manager import CooldownManager
from audio.message_formatter import identity_message, danger_message, emotion_message, ocr_message

logger = logging.getLogger(__name__)


class SpeechManager:
    def __init__(self, audio_queue):
        self.audio = audio_queue
        self.cooldowns = CooldownManager()

    def on_object_result(self, payload):
        for det in payload.get('detections', []):
            if det['label'] in OBJECT['danger_classes'] and det['area_ratio'] >= OBJECT['near_area_ratio']:
                key = f'danger:{det["label"]}'
                if self.cooldowns.ready_and_hit(key, RULES['danger_cooldown_sec']):
                    self.audio.push(danger_message(det['label']), PRIORITY['danger'], key, interrupt=True)

    def on_face_result(self, payload):
        face = payload.get('recognized_face')
        if not face:
            return
        name = face['name']
        if name == 'unknown':
            key = 'identity:unknown'
            cooldown = RULES['unknown_person_cooldown_sec']
        else:
            key = f'identity:{name}'
            cooldown = FACE['speak_identity_cooldown_sec']
        if self.cooldowns.ready_and_hit(key, cooldown):
            self.audio.push(identity_message(name), PRIORITY['identity'], key)

    def on_emotion_result(self, payload):
        key = f'emotion:{payload["name"]}:{payload["emotion"]}'
        if self.cooldowns.ready_and_hit(key, EMOTION['cooldown_sec']):
            self.audio.push(emotion_message(payload['name'], payload['emotion']), PRIORITY['info'], key)

    def on_ocr_result(self, payload):
        text = payload.get('text', '').strip()
        if len(text) < 3:
            return
        key = f'ocr:{text[:40]}'
        if self.cooldowns.ready_and_hit(key, OCR['cooldown_sec']):
            self.audio.push(ocr_message(text), PRIORITY['ocr'], key)

    def on_system_error(self, payload):
        key = 'system_error'
        if self.cooldowns.ready_and_hit(key, 10.0):
            self.audio.push('System warning', PRIORITY['danger'], key)
