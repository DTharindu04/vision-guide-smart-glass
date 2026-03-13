from __future__ import annotations
import argparse
import json
import time
from pathlib import Path

import cv2
import numpy as np

from config import FACE, PATHS
from camera.camera_stream import CameraStream
from camera.camera_utils import variance_of_laplacian


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--samples', type=int, default=150)
    parser.add_argument('--interval', type=float, default=0.15)
    args = parser.parse_args()

    detector = cv2.FaceDetectorYN.create(FACE['detector_path'], '', FACE['input_size'], FACE['score_thres'], FACE['nms_thres'], FACE['top_k'])
    out_dir = Path('data/faces/raw') / args.name
    out_dir.mkdir(parents=True, exist_ok=True)

    cam = CameraStream().start()
    captured = 0
    last = 0.0
    print(f'[INFO] Collecting {args.samples} samples for {args.name}')
    try:
        while captured < args.samples:
            frame = cam.read()
            if frame is None:
                continue
            h, w = frame.shape[:2]
            detector.setInputSize((w, h))
            _, faces = detector.detect(frame)
            if faces is None or len(faces) == 0:
                cv2.imshow('Enroll', frame)
                if cv2.waitKey(1) == 27:
                    break
                continue
            face = max(faces, key=lambda f: f[2] * f[3])
            x, y, fw, fh = face[:4].astype(int)
            patch = frame[y:y+fh, x:x+fw]
            if patch.size == 0:
                continue
            if variance_of_laplacian(patch) < FACE['clear_face_var_thres']:
                continue
            if time.time() - last < args.interval:
                continue
            last = time.time()
            cv2.imwrite(str(out_dir / f'{captured:04d}.jpg'), patch)
            captured += 1
            vis = frame.copy()
            cv2.rectangle(vis, (x, y), (x+fw, y+fh), (0, 255, 0), 2)
            cv2.putText(vis, f'{captured}/{args.samples}', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.imshow('Enroll', vis)
            cv2.waitKey(1)
    finally:
        cam.stop()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
