import os

import logger
from backup import Backup


def compress(backup: Backup) -> None:
    destfile: str = os.path.join(backup.destination, backup.filename)

    command = f'tar -PI "zstd -19 -T0" -cf "{destfile}" '
    command += " ".join(f'"{x}"' for x in backup.children)
    code = os.system(command)
    if code != 0:
        logger.error(f'Compression exits with code {code}!')
        exit(code)
