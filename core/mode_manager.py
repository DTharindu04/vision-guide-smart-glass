class ModeManager:
    def __init__(self):
        self.mode = 'navigation'
        self.reading_mode = False

    def set_mode(self, mode: str):
        self.mode = mode
        self.reading_mode = mode == 'reading'

    def toggle_reading(self):
        self.reading_mode = not self.reading_mode
        self.mode = 'reading' if self.reading_mode else 'navigation'
        return self.mode
