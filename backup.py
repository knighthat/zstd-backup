#!/usr/bin/python3
import os
from file import File
from sys import argv, exit as code
from re import match
from datetime import datetime, timedelta as delta
from unit_converter import BytesConverter
from subprocess import run


def abspath(path: str) -> str:
    if path.startswith("~"):
        path = os.path.expanduser(path)
    if not path.startswith("/") or path.startswith("."):
        path = os.path.join(os.curdir, path)
    return os.path.abspath(path)


def set_destination() -> str:
    while True:
        user_dest = input("Where do you want to save this? ")
        abs_path = abspath(user_dest)
        if os.path.exists(abs_path):
            if not os.path.isdir(abs_path):
                print(f"{user_dest} is not a folder!")
            else:
                break
        else:
            print(f"{abs_path} does not exist!")
    return user_dest


def include() -> list[str]:
    incld_tmp = []
    while True:
        user_in = input("What file/folder shall be included? (Leave empty to end)")
        if len(user_in) == 0:
            break
        abs_path = abspath(user_in)
        incld_tmp.append(abs_path)
    return incld_tmp

def get_old_backups() -> list[str]:
    backups = []
    backup_name_format = r'^\w{3}-\d{2}-\d{4}.zstd'
    for name in os.listdir(dest):
        if match(backup_name_format, name):
            backups.append(name)
    return backups


def delete_overtime(backups: list[str], t: int = 90) -> None:
    def parse_date(date: str) -> datetime:
        if date.endswith("zstd"):
            date = os.path.splitext(date)[0]
        return datetime.strptime(date, "%b-%d-%Y")

    period = delta(days=t)
    for name in backups:
        if time_now - parse_date(name) > period:
            os.remove(os.path.join(dest, name))
            backups.remove(name)


time_now = datetime.now()
dest: str = abspath(argv[1]) if len(argv) >= 2 else set_destination()
includes: list[str] = argv[2:] if len(argv) >= 3 else include()
exceptions: list[str] = []


if __name__ == '__main__':
    old_backups = get_old_backups()
    if len(old_backups) > 0:
        delete_overtime(old_backups)

    file = File(includes, dest, time_now)
    exceptions.extend(file.verify_children())

    dest_stat = os.statvfs(dest)
    free_space = dest_stat.f_frsize * dest_stat.f_bavail
    if free_space < file.size:
        estimate_str = BytesConverter(file.size).__str__()
        exceptions.append(f"Not enough space! Requires at least {estimate_str}")
    else:
        # tar -PI "zstd -19 -T0"
        cmd = ["tar", "-PI", "zstd --ultra -22 -T0", "-cf", file.abspath(), " ".join(file.children)]
        exit_code = run(cmd).returncode

    print(f'Exit code: {exit_code}')
    print(f"Exceptions: {exceptions}")