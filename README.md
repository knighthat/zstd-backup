<h1 align="center">ZSTD BACKUP</h1>
<p align="center">Backup your files and folders using ZSTD compression algorithm</p>

# Why Zstandard (ZSTD)

Zstandard (ZSTD) provides the best compression ratio (as far as I know). \
Furthermore, the algorithm also allows multithreading for faster compression while being easy to use
and is compatible with tar command

# Installation

## Requirements

1. Linux machine
2. Tar package (most linux distros come with this)
3. Python 3.11 (also included in most modern distros)
4. Git
    * Debian-based distros (Debian, Ubuntu, Mint, etc.): `apt install git`
    * RedHat-based distros (Red Hat, Fedora, CentOS, etc.): `dnf install git`
    * Arch-based distros (Arch Linux, Manjaro): `pacman -S git`
5. ZSTD package
    * Debian-based distros (Debian, Ubuntu, Mint, etc.): `apt install zstd`
    * RedHat-based distros (Red Hat, Fedora, CentOS, etc.): `dnf install zstd`
    * Arch-based distros (Arch Linux, Manjaro): `pacman -S zstd`

## Setup

1. Clone this repo

```shell
git clone https://github.com/knighthat/linux-server-backup
```

2. Create virtual environment (recommended, or use global python env)

```shell
/usr/share/python3 -m venv venv
```

3. Install required packages

```shell
/path/to/venv/bin/pip install -r requirements.txt
```

4. Edit configuration `config.yml`
5. Run program by executing `main.py` script

```shell
/path/to/env/bin/python3 main.py
```

# Issues

If you have any question, please open a ticket [HERE](https://github.com/knighthat/linux-server-backup/issues)

# License

This repo is licensed under MIT. Feel free to use, modify, and re-distribute without any restriction.