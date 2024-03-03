<h1 align="center">ZSTD BACKUP</h1>
<p align="center">Backup your files and folders using ZSTD compression algorithm</p>

# Why Zstandard (ZSTD)

Zstandard (ZSTD) provides the best compression ratio (as far as I know). \
Furthermore, the algorithm also allows multithreading for faster compression while being easy to use
and is compatible with tar command

For more details, visit [facebook/zstd](https://github.com/facebook/zstd)

# Installation

## Requirements

1. Python 3.11
    - Linux: Included in most modern distros
    - [Windows](https://www.python.org/downloads/windows/)
    - [MacOS](https://www.python.org/downloads/macos/)
2. Git
    * Debian-based distros (Debian, Ubuntu, Mint, etc.): `apt install git`
    * RedHat-based distros (Red Hat, Fedora, CentOS, etc.): `dnf install git`
    * Arch-based distros (Arch Linux, Manjaro): `pacman -S git`
    * [Git for Windows](https://git-scm.com/download/win)
    * [Git for macOS](https://git-scm.com/download/mac)

## Setup

1. Clone this repo

```shell
git clone --depth 1 https://github.com/knighthat/zstd-backup && cd zstd-backup
```

2. Create virtual environment (recommended, or use global python)

### Windows

> Run this in your command prompt or powershell

```shell
python -m venv venv
```

### Linux

```shell
/usr/bin/python3 -m venv venv
```

### MacOS

```shell
python -m venv venv
```

3. Install required packages

```shell
venv/bin/pip install -r requirements.txt
```

4. Edit configuration [config.yml](#configyml)
5. Run program by executing `main.py` script

### Windows

```shell
venv\Scripts\python zstd_backup.py
```

### Others

```shell
venv/bin/python3 main.py
```

## config.yml

> This is where you specify the files/folders that are included in the compressed file.  
> Also the place where compressed file saved to.

```yaml
# Available levels: DEBUG, INFO, WARN, ERROR, FATAL
console_log_level: INFO

# All files and folders will be included
# in the final compressed file.
include:
  - "./test"

# Where to save this backup.
# Must be a path (program creates dirs if path not exist)
destination: "./backups"

# Ignore all files that start with 1 of the paths below.
# Must be in absolute form.
# If '/path/to/ignore' is listed, any sub-folders and files
# within that directory will be ignored.
ignore:
  - '/path/to/ignore1'
  - '/path/to/ignore2'
  - '/path/to/ignore3'

old_backups:
  # How many backups should I keep (default: 5, 0 means unlimited)
  keep: 5
  # If a backup's creation date exceeds this number, it'll be deleted.
  # Set this to 0 to skip this process
  retention: 30   # Days
  # Should this program delete older backups (even if it was
  # within retention days and total files less than 'keep')
  # to save space for new backup.
  # This option always keeps the most recent backup
  # unless 'aggressive' is set to True.
  remove_old_backups_for_space: true
  # If True, delete to the last backup to make some space for new backup
  aggressive: false

arguments:
  # Compression level.
  # Higher values are slower but yield smaller size.
  # Default level is 3
  # More at: https://python-zstandard.readthedocs.io/en/latest/compressor.html#zstdcompressor
  level: 3
  # How many should the algo use.
  # More threads equals faster compression time.
  # 0 will use all threads (also the default)
  threads: 4
```

# Issues

If you have any question, please open a ticket [HERE](https://github.com/knighthat/linux-server-backup/issues)

# License

This repo is licensed under MIT. Feel free to use, modify, and re-distribute without restrictions.