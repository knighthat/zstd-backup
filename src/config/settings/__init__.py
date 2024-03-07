from .ProgressBar import ProgressBar


class Settings:
    write_chunk: int = 1024
    progress_bar: ProgressBar

    def __init__(self, settings: dict):
        self.progress_bar = ProgressBar(settings['progress_bar'])
