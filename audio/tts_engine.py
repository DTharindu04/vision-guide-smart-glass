from __future__ import annotations
import os
import subprocess
import tempfile
import wave
import logging
from pathlib import Path

from config import AUDIO

logger = logging.getLogger(__name__)


class TTSEngine:
    def __init__(self):
        self.engine = AUDIO['engine']
        self.enabled = AUDIO['enabled']

    def speak(self, text: str):
        if not self.enabled or not text:
            return
        if self.engine == 'piper' and Path(AUDIO['piper_model']).exists():
            self._speak_piper(text)
        else:
            self._speak_espeak(text)

    def _speak_piper(self, text: str):
        wav_path = tempfile.mktemp(suffix='.wav')
        cmd = [
            AUDIO['piper_bin'],
            '--model', AUDIO['piper_model'],
            '--output_file', wav_path,
        ]
        subprocess.run(cmd, input=text.encode('utf-8'), check=True)
        subprocess.run(['aplay', '-q', wav_path], check=False)
        try:
            os.remove(wav_path)
        except OSError:
            pass

    def _speak_espeak(self, text: str):
        subprocess.run(['espeak-ng', '-v', AUDIO['espeak_voice'], text], check=False)
