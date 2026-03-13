from __future__ import annotations
import json
from pathlib import Path
import cv2
import numpy as np

from config import FACE, PATHS


def augment(img):
    out = [img]
    out.append(cv2.flip(img, 1))
    out.append(cv2.convertScaleAbs(img, alpha=1.1, beta=5))
    out.append(cv2.GaussianBlur(img, (3, 3), 0))
    return out


def main():
    raw_root = Path('data/faces/raw')
    recog = cv2.FaceRecognizerSF.create(FACE['recognizer_path'], '')
    embeddings = []
    names = []

    for person_dir in sorted(raw_root.glob('*')):
        if not person_dir.is_dir():
            continue
        name = person_dir.name
        for img_path in sorted(person_dir.glob('*.jpg')):
            img = cv2.imread(str(img_path))
            if img is None:
                continue
            for aug in augment(img):
                aligned = cv2.resize(aug, (112, 112))
                emb = recog.feature(aligned).flatten().astype(np.float32)
                embeddings.append(emb)
                names.append(name)

    if not embeddings:
        raise RuntimeError('No embeddings generated. Run enroll_faces.py first.')

    np.savez(PATHS['face_embeddings'], embeddings=np.stack(embeddings))
    Path(PATHS['face_metadata']).write_text(json.dumps({'names': names}, indent=2))
    print(f'Saved {len(names)} embeddings')


if __name__ == '__main__':
    main()
