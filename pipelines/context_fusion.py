from __future__ import annotations


def summarize_scene(detections):
    labels = [d['label'] for d in detections]
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    return counts
