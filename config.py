from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / 'models'
DATA_DIR = BASE_DIR / 'data'
LOG_DIR = BASE_DIR / 'logs'
FACE_DB_DIR = DATA_DIR / 'faces'
AUDIO_TMP_DIR = BASE_DIR / 'audio_tmp'
AUDIO_TMP_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
FACE_DB_DIR.mkdir(parents=True, exist_ok=True)

APP_NAME = 'smart_glasses_pi'
DEBUG = True

CAMERA = {
    'main_size': (640, 480),
    'lores_size': (320, 240),
    'fps': 20,
    'flip': False,
    'buffer_size': 4,
    'empty_frame_sleep': 0.01,
}

SCHEDULER = {
    'loop_hz': 10,
    'max_cpu_temp_c': 80.0,
    'high_cpu_backoff_sec': 0.2,
}

OBJECT = {
    'enabled': True,
    'model_path': str(MODELS_DIR / 'yolov8n.onnx'),
    'input_size': 320,
    'conf_thres': 0.45,
    'nms_thres': 0.50,
    'run_every_n_frames': 2,
    'person_class_names': {'person'},
    'urgent_classes': {'person', 'car', 'bus', 'truck', 'motorcycle', 'bicycle', 'dog'},
    'danger_classes': {'car', 'bus', 'truck', 'motorcycle', 'bicycle'},
    'near_area_ratio': 0.18,
}

FACE = {
    'enabled': True,
    'detector_path': str(MODELS_DIR / 'face_detection_yunet_2023mar.onnx'),
    'recognizer_path': str(MODELS_DIR / 'face_recognition_sface_2021dec.onnx'),
    'input_size': (320, 240),
    'score_thres': 0.75,
    'nms_thres': 0.30,
    'top_k': 500,
    'min_face_size': 60,
    'trigger_person_cooldown_sec': 1.5,
    'recognition_threshold': 0.38,
    'clear_face_var_thres': 70.0,
    'frontal_max_eye_delta_ratio': 0.15,
    'speak_identity_cooldown_sec': 10.0,
}

EMOTION = {
    'enabled': True,
    'model_path': str(MODELS_DIR / 'emotion_ferplus.onnx'),
    'input_size': (64, 64),
    'conf_thres': 0.55,
    'run_every_n_recognized_frames': 8,
    'cooldown_sec': 12.0,
    'labels': ['neutral', 'happiness', 'surprise', 'sadness', 'anger', 'disgust', 'fear', 'contempt'],
}

OCR = {
    'enabled': True,
    'language': 'eng',
    'psm': 6,
    'min_text_area': 0.02,
    'cooldown_sec': 15.0,
    'max_chars_spoken': 120,
    'trigger_interval_sec': 1.0,
}

AUDIO = {
    'enabled': True,
    'engine': 'piper',  # piper | espeak
    'piper_bin': 'piper',
    'piper_model': str(MODELS_DIR / 'tts' / 'en_US-lessac-medium.onnx'),
    'piper_config': str(MODELS_DIR / 'tts' / 'en_US-lessac-medium.onnx.json'),
    'espeak_voice': 'en',
    'sample_rate': 22050,
    'queue_maxsize': 64,
    'dedupe_window_sec': 6.0,
}

PRIORITY = {
    'danger': 0,
    'identity': 1,
    'ocr': 2,
    'info': 3,
}

RULES = {
    'unknown_person_cooldown_sec': 12.0,
    'danger_cooldown_sec': 4.0,
    'low_light_brightness_thres': 55.0,
    'blurry_var_thres': 55.0,
    'max_faces_per_frame': 3,
}

PATHS = {
    'face_embeddings': str(FACE_DB_DIR / 'embeddings.npz'),
    'face_metadata': str(FACE_DB_DIR / 'metadata.json'),
    'events_log': str(LOG_DIR / 'events.log'),
}

CLASS_NAMES = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
    'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
    'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
    'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
    'hair drier', 'toothbrush'
]
