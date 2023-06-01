#!/usr/bin/python3
import os
from sys import argv, exit as code
from re import match
from datetime import datetime, timedelta as delta
from unit_converter import BytesConverter
from subprocess import run


class Exceptions:
    def __init__(self) -> None:
        pass


def abs(path: str) -> str:
    if path.startswith("~"):
        path = os.path.expanduser(path)
    return os.path.abspath(path)


def exists(path: str) -> bool:
    if not os.path.exists(path):
        print(f"{path} does not exist!")
    return os.path.exists(path)


def set_destination() -> str:
    while True:
        user_dest = input("Where do you want to save this? ")
        abs_path = abs(user_dest)
        if exists(abs_path):
            if not os.path.isdir(abs_path):
                print(f"{user_dest} is not a folder!")
                code(3)
            else:
                break
    return user_dest


def include() -> list[str]:
    incld_tmp = []
    while True:
        user_in = input("What file/folder shall be included? (Leave empty to end)")
        if len(user_in) == 0:
            break
        abs_path = abs(user_in)
        if exists(abs_path):
            incld_tmp.append(abs_path)
    return incld_tmp


def parse_date(date: str) -> datetime:
    if date.endswith("zstd"):
        date = os.path.splitext(date)[0]
    return datetime.strptime(date, "%b-%d-%Y")


def get_old_backups() -> list[str]:
    backups = []
    backup_name_format = r'^\w{3}-\d{2}-\d{4}.zstd'
    for path, ignored, files in os.walk(dest):
        for name in files:
            if match(backup_name_format, name):
                backups.append(name)
    return backups


def delete_overtime(backups: list[str], t: int = 90) -> None:
    period = delta(days=t)

    for name in backups:
        if time_now - parse_date(name) > period:
            os.remove(os.path.join(dest, name))
            backups.remove(name)


def delete_oldest(backups: list[str]):
    backups.sort(key=lambda x: parse_date(x))
    oldest = backups[-1]
    os.remove(os.path.join(dest, oldest))
    backups.remove(oldest)


def get_output_estimate() -> int:
    result = 1024**3  # 1 GiB overhead
    for file in includes:
        result += os.path.getsize(file)
    return result


time_now = datetime.now()
dest: str = abs(argv[1]) if len(argv) >= 2 else set_destination()
includes: list[str] = argv[2:] if len(argv) >= 3 else include()


if __name__ == '__main__':
    old_backups = get_old_backups()
    if len(old_backups) > 0:
        delete_overtime(old_backups)

    dest_stat = os.statvfs(dest)
    estimate = get_output_estimate()

    writable = dest_stat.f_frsize * dest_stat.f_bavail > estimate
    while not writable:
        if len(old_backups) > 0:
            delete_oldest(old_backups)
        else:
            estimate_str = BytesConverter(estimate).__str__()
            print(f"Not enough space! Requires at least {estimate_str}")
            exit(1)
        writable = dest_stat.f_frsize * dest_stat.f_bavail > estimate

    # tar -PI "zstd -19 -T0"
    output_name = time_now.strftime("%b-%d-%Y") + ".zstd"
    output_file = os.path.join(dest, output_name)
    cmd = ["tar", "-PI", "zstd --ultra -22 -T0", "-cf", output_file, " ".join(includes)]
    print(cmd)
    exit_code = run(cmd).returncode
    print(exit_code)
