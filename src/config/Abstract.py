class ConfigTemplate:
    _configuration: dict

    def __init__(self, configuration: dict) -> None:
        self._configuration = configuration

    def __exist__(self, item: str) -> bool:
        return item in self._configuration

    def __getitem__(self, item: str):
        if not self.__exist__(item):
            raise KeyError(f'\'{item}\' does NOT exist!')
        return self._configuration[item]
