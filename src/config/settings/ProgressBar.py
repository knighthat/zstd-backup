class ProgressBar:
    enabled: bool = False

    def __init__(self, configuration: dict) -> None:
        self.enabled = configuration['enabled']
