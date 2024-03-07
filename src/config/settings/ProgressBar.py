class ProgressBar:
    enabled: bool = False

    def __init__(self, configuration: dict):
        self.enabled = configuration['enabled']
