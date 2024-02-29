import os
import tarfile

import zstandard as zstd

from src.backup import BackupProfile
from src.config import Configuration


def zstd_compress(profile: BackupProfile, config: Configuration) -> None:
    with open(os.path.join(profile.destination, profile.filename), 'wb') as zfile:
        # Add file to TAR while compressing it
        def _compress(file: str) -> None:
            tar.add(file)

        # Walk through all files inside a folder
        # and add it to TAR using _compress()
        def _compress_dir(folder: str) -> None:
            for root, paths, files in os.walk(folder):
                for name in files:
                    _compress(os.path.join(root, name))

        # Create zstd file and its stream to write data
        cctx = zstd.ZstdCompressor(level=config.zstd_arguments.level, threads=config.zstd_arguments.threads)
        cstream = cctx.stream_writer(zfile)

        # Use TAR to store multiple files while
        # keeping their absolute paths
        with tarfile.open(fileobj=cstream, mode='w|', format=tarfile.PAX_FORMAT) as tar:

            for child in profile.children:
                if os.path.isfile(child):
                    _compress(child)

                if os.path.isdir(child):
                    _compress_dir(child)

        # Flush stream (finalize the file)
        cstream.flush(zstd.FLUSH_FRAME)
