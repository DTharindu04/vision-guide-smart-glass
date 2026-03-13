from __future__ import annotations
import logging
import time
import traceback
import cv2

from config import SCHEDULER, OBJECT, FACE, EMOTION, OCR

logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self, camera, decision_engine, app_state, object_pipeline, face_pipeline, emotion_pipeline, ocr_pipeline, event_bus, health_monitor):
        self.camera = camera
        self.decision_engine = decision_engine
        self.app_state = app_state
        self.object_pipeline = object_pipeline
        self.face_pipeline = face_pipeline
        self.emotion_pipeline = emotion_pipeline
        self.ocr_pipeline = ocr_pipeline
        self.event_bus = event_bus
        self.health_monitor = health_monitor

    def run(self):
        sleep_dt = 1.0 / max(1, SCHEDULER['loop_hz'])
        while self.app_state.running:
            started = time.time()
            try:
                frame = self.camera.read()
                if frame is None:
                    time.sleep(0.02)
                    continue
                self.app_state.stats.frame_id += 1
                frame_id = self.app_state.stats.frame_id
                self.app_state.update(last_frame_ts=time.time())

                health = self.health_monitor.sample()
                self.app_state.update(last_health=health)
                if 0 < health.get('cpu_temp_c', -1) >= SCHEDULER['max_cpu_temp_c']:
                    logger.warning('CPU temp high: %.1fC', health['cpu_temp_c'])
                    time.sleep(SCHEDULER['high_cpu_backoff_sec'])

                state = self.app_state.snapshot()
                plan = self.decision_engine.plan(frame_id, frame, state)
                self.app_state.update(low_light=plan.brightness < 55.0, blurry=plan.blur_score < 55.0)

                if plan.run_object and OBJECT['enabled']:
                    obj = self.object_pipeline.run(frame, frame_id)
                    self.app_state.stats.object_runs += 1
                    self.app_state.update(last_object_result=obj)
                    self.event_bus.publish('object_result', obj)

                if plan.run_face and FACE['enabled']:
                    face = self.face_pipeline.run(frame, plan.face_rois, frame_id)
                    self.app_state.stats.face_runs += 1
                    self.app_state.update(last_face_result=face)
                    self.event_bus.publish('face_result', face)

                if plan.run_emotion and EMOTION['enabled']:
                    emo = self.emotion_pipeline.run(frame, self.app_state.last_face_result, frame_id)
                    if emo:
                        self.app_state.stats.emotion_runs += 1
                        self.event_bus.publish('emotion_result', emo)

                if plan.run_ocr and OCR['enabled']:
                    ocr = self.ocr_pipeline.run(frame, frame_id)
                    if ocr:
                        self.app_state.stats.ocr_runs += 1
                        self.app_state.update(last_ocr_text=ocr.get('text', ''))
                        self.event_bus.publish('ocr_result', ocr)

            except KeyboardInterrupt:
                self.app_state.running = False
            except Exception as exc:
                logger.error('Scheduler error: %s', exc)
                logger.debug(traceback.format_exc())
                self.event_bus.publish('system_error', {'error': str(exc)})
                time.sleep(0.1)
            finally:
                elapsed = (time.time() - started) * 1000.0
                s = self.app_state.stats
                s.avg_loop_ms = 0.9 * s.avg_loop_ms + 0.1 * elapsed if s.avg_loop_ms else elapsed
                to_sleep = max(0.0, sleep_dt - (time.time() - started))
                time.sleep(to_sleep)
