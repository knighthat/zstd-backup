import os
import tarfile
from io import BytesIO

import zstandard as zstd
from tqdm import tqdm

from src.backup import BackupProfile
from src.config import Configuration


def compress(children: set, writer: zstd.ZstdCompressionWriter, epb: bool, chunk_size: int, total_size: int = 0) -> None:
    """
    Compress data of each files from children.
    To enable progress bar, set 'epb' to True.

    :param children: set of file paths to write
    :param writer: Stream to be written data into
    :param epb: Show progress bar (beta)
    :param chunk_size: How many bytes to write per cycle
    :param total_size: Total size for progress bar
    :return:
    """

    " Use TAR to store multiple files while keeping their absolute paths "
    tar: tarfile.TarFile = tarfile.open(fileobj=writer, mode='w|', format=tarfile.PAX_FORMAT)

    if epb:
        " Init progress bar "
        progress_bar: tqdm = tqdm(total=total_size, desc="Compressing", unit='iB', unit_scale=True)

        for filepath in children:
            file = open(filepath, 'rb')
            while True:
                """
                For each loop, read a portion of the file.
                Break if there's nothing to read
                """
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                " TarInfo helps trimming chunk down if data is less than chunk size "
                tarinfo = tarfile.TarInfo(name=filepath)
                tarinfo.size = len(chunk)

                " Add chunk to TAR "
                tar.addfile(tarinfo, fileobj=BytesIO(chunk))
                " Update progress bar"
                progress_bar.update(tarinfo.size)

            file.close()
    else:

        for filepath in children:
            tar.add(filepath)

    tar.close()
    # Flush stream (finalize the file)
    writer.flush(zstd.FLUSH_FRAME)


def zstd_compress(profile: BackupProfile, config: Configuration) -> None:
    with open(os.path.join(profile.destination, profile.filename), 'wb') as zfile:
        # Create zstd file and its stream to write data
        cctx = zstd.ZstdCompressor(level=config.zstd_arguments.level, threads=config.zstd_arguments.threads)
        cstream = cctx.stream_writer(zfile)

        compress(
            profile.children,
            cstream,
            config.settings.progress_bar.enabled,
            config.settings.write_chunk,
            len(profile)
        )
