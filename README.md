<h1 align="center">ZSTD BACKUP</h1>
<p align="center">Backup your files and folders using ZSTD compression algorithm</p>

# Why Zstandard (ZSTD)

Zstandard (ZSTD) provides the best compression ratio (as far as I know). \
Furthermore, the algorithm also allows multithreading for faster compression while being easy to use
and is compatible with tar command

For more details, visit [facebook/zstd](https://github.com/facebook/zstd)

# Installation

## Requirements

1. Linux machine
2. Tar package (most linux distros come with this)
3. Python 3.11 (also included in most modern distros)
4. Git
    * Debian-based distros (Debian, Ubuntu, Mint, etc.): `apt install git`
    * RedHat-based distros (Red Hat, Fedora, CentOS, etc.): `dnf install git`
    * Arch-based distros (Arch Linux, Manjaro): `pacman -S git`

## Setup

1. Clone this repo

```shell
git clone --depth 1 https://github.com/knighthat/zstd-backup && cd zstd-backup
```

2. Create virtual environment (recommended, or use global python)

```shell
/usr/share/python3 -m venv venv
```

3. Install required packages

```shell
venv/bin/pip install -r requirements.txt
```

4. Edit configuration `config.yml`
5. Run program by executing `main.py` script

```shell
env/bin/python3 main.py
```

## config.yml

> This is where you specify the files/folders that are included in the compressed file.  
> Also the place where compressed file saved to.

```yaml
# Available levels: DEBUG, INFO, WARN, ERROR, FATAL
console_log_level: INFO

# How many backups should I keep (default: 5, 0 means unlimited)
keep: 5

include:
  - "test"

destination: "./backups"

# Ignore all files that start
# with 1 of the paths below.
ignore:
  - '/path/to/ignore'

delete_older_than: 30   # days
# If true, program will remove backups
# (from oldest to newest) one by until
# there's enough space for new backup
# NOTE: it will stop at last backup
# to prevent data lost.
remove_old_backups_for_space: true

arguments:
  # Compression level.
  # Higher values are slower but yield smaller size.
  # Default level is 3
  # More at: https://python-zstandard.readthedocs.io/en/latest/compressor.html#zstdcompressor
  level: 3
  # How many should the algo use.
  # More threads equals faster compression time.
  # 0 will use all threads (also the default)
  threads: 0
```

# Issues

If you have any question, please open a ticket [HERE](https://github.com/knighthat/linux-server-backup/issues)

# License

This repo is licensed under MIT. Feel free to use, modify, and re-distribute without restrictions.