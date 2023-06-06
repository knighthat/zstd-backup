from os.path import getsize, join, exists, isdir
from os import access, R_OK, listdir
from datetime import datetime


class File:
    def __init__(self, children: list[str], dest: str, time: datetime) -> None:
        self.ext = "zstd"
        self.name = time.strftime("%b-%d-%Y")
        self.children = children
        self.dest = dest
        self.size = self._getsize()

    def _getsize(self) -> int:
        result = 1024 ** 3  # 1 GiB overhead
        for file in self.children:
            result += getsize(file)
        return result

    def full_name(self) -> str:
        return f'{self.name}.{self.ext}'

    def abspath(self) -> str:
        return join(self.dest, self.full_name())

    def verify_children(self) -> list[str]:
        exceptions = []
        for child in self.children.copy():
            if not exists(child):
                exceptions.append(f"{child} does not exist!")
                self.children.remove(child)
            elif not access(child, R_OK):
                exceptions.append(f"Cannot access {child}")
                self.children.remove(child)
            elif isdir(child) and len(listdir(child)) == 0:
                exceptions.append(f"{child} is empty!")
                self.children.remove(child)
        return exceptions
