class BytesConverter:
    def __init__(self, number: int) -> None:
        TB, GB, MB, KB, B = 0, 0, 0, 0, number
        if B > 1024:
            KB, B = divmod(number, 1024)
        if KB >= 1024:
            MB, KB = divmod(KB, 1024)
        if MB >= 1024:
            GB, MB = divmod(MB, 1024)
        if GB >= 1024:
            TB, GB = divmod(GB, 1024)

        self.TB = TB
        self.GB = GB
        self.MB = MB
        self.KB = KB
        self.B = B

    def __getB__(self) -> int:
        return self.B

    def __getK__(self) -> int:
        return self.KB

    def __getM__(self) -> int:
        return self.MB

    def __getG__(self) -> int:
        return self.GB

    def __getT__(self) -> int:
        return self.TB

    def __str__(self) -> str:
        result = []
        if self.TB > 0:
            result.append(f"{self.TB} Terabyte{'' if self.TB == 1 else 's'}")
        if self.GB > 0:
            result.append(f"{self.GB} Gigabyte{'' if self.GB == 1 else 's'}")
        if self.MB > 0:
            result.append(f"{self.MB} Megabyte{'' if self.MB == 1 else 's'}")
        if self.KB > 0:
            result.append(f"{self.KB} Kilobyte{'' if self.KB == 1 else 's'}")
        if self.B > 0:
            result.append(f"{self.B} Byte{'' if self.B == 1 else 's'}")

        return " ".join(result)
