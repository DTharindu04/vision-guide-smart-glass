Place the following files under `models/`:

- `yolov8n.onnx`
- `face_detection_yunet_2023mar.onnx`
- `face_recognition_sface_2021dec.onnx`
- `emotion_ferplus.onnx`
- `tts/en_US-lessac-medium.onnx`
- `tts/en_US-lessac-medium.onnx.json`

Recommended sources:
- Object detection: export YOLO nano model to ONNX/NCNN from Ultralytics docs.
- Face detection / recognition / emotion: OpenCV Zoo ONNX models.
- TTS: Piper voice model.
