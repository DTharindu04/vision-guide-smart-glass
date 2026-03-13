from __future__ import annotations
import signal
import logging

from config import PATHS
from utils.logging_utils import setup_logging
from core.app_state import AppState
from core.event_bus import EventBus
from core.mode_manager import ModeManager
from core.health_monitor import HealthMonitor
from core.decision_engine import DecisionEngine
from core.scheduler import Scheduler
from camera.camera_stream import CameraStream
from pipelines.object_pipeline import ObjectPipeline
from pipelines.face_pipeline import FacePipeline
from pipelines.emotion_pipeline import EmotionPipeline
from pipelines.ocr_pipeline import OCRPipeline
from audio.tts_engine import TTSEngine
from audio.audio_queue import AudioQueue
from audio.speech_manager import SpeechManager


def main():
    setup_logging(PATHS['events_log'])
    logger = logging.getLogger('main')
    app_state = AppState()
    event_bus = EventBus()
    mode_manager = ModeManager()
    health_monitor = HealthMonitor()
    decision_engine = DecisionEngine()

    camera = CameraStream().start()
    object_pipeline = ObjectPipeline()
    face_pipeline = FacePipeline()
    emotion_pipeline = EmotionPipeline()
    ocr_pipeline = OCRPipeline()

    tts = TTSEngine()
    audio_queue = AudioQueue(tts, app_state)
    speech = SpeechManager(audio_queue)

    event_bus.subscribe('object_result', speech.on_object_result)
    event_bus.subscribe('face_result', speech.on_face_result)
    event_bus.subscribe('emotion_result', speech.on_emotion_result)
    event_bus.subscribe('ocr_result', speech.on_ocr_result)
    event_bus.subscribe('system_error', speech.on_system_error)

    def handle_signal(*_):
        logger.info('Shutdown requested')
        app_state.running = False

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    event_bus.start()
    audio_queue.start()

    scheduler = Scheduler(
        camera=camera,
        decision_engine=decision_engine,
        app_state=app_state,
        object_pipeline=object_pipeline,
        face_pipeline=face_pipeline,
        emotion_pipeline=emotion_pipeline,
        ocr_pipeline=ocr_pipeline,
        event_bus=event_bus,
        health_monitor=health_monitor,
    )

    logger.info('Smart glasses app started in %s mode', mode_manager.mode)
    try:
        scheduler.run()
    finally:
        logger.info('Stopping services')
        camera.stop()
        event_bus.stop()
        audio_queue.stop()


if __name__ == '__main__':
    main()
