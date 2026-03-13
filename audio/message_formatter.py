from __future__ import annotations


def identity_message(name: str) -> str:
    return f'{name} ahead' if name != 'unknown' else 'Unknown person ahead'


def danger_message(label: str) -> str:
    return f'Warning. {label} ahead.'


def emotion_message(name: str, emotion: str) -> str:
    who = name if name != 'unknown' else 'Person'
    return f'{who} looks {emotion}'


def ocr_message(text: str) -> str:
    return f'Text says: {text}'
