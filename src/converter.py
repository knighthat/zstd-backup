import math

from src.logger import debug


# Credit to ['vallentin', 'James Sapam'] from Stack Overflow
# https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
def size_converter(size_b: int) -> str:
    """
    Convert given bytes into comprehensive unit.
    Support wide range of units from byte(B) to yottabyte(YB)

    Context: 1 yottabyte is 1024 to the power of 8 (~1E+24)

    :param size_b: size of file in bytes
    :return: comprehensive number with unit signature
    """

    if size_b == 0:
        return "0B"

    " Define supported units "
    units = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')

    " Get the exponent of size_b to which 1024 must be raised to "
    exponent: float = math.log(size_b, 1024)
    " This function supports up to 9 units. This is the limiter "
    exponent = min(9, math.floor(exponent))
    " Get the position of unit based on the exponent "
    position = int(exponent)
    """
    Get the equivalent bytes of that unit
    E.g. 1KB = 1024 bytes, 1MB = 1,048,576 bytes, etc. 
    """
    unit_b: float = math.pow(1024, position)
    " Convert size_b to defined unit (rounded to the hundredth) "
    size: float = round(size_b / unit_b, 2)

    " Result follows format '00.00 MB' "
    result: str = f'{size} {units[position]}'
    debug(f'Converted {size_b} bytes to {result}')

    return result


def time_converter(seconds: float) -> str:
    """
    Convert given seconds into easier to read form (hours, minutes, seconds).

    :param seconds: time to convert
    :return: hours, minutes, and seconds if any has value greater than 0
    """
    hour, second = divmod(round(seconds), 3600)
    " Define time units "
    units: dict[str, int] = {
        'hour': hour,
        'minute': 0,
        'second': second
    }
    if units['second'] >= 60:
        units['minute'], units['second'] = divmod(units['second'], 60)

    " String builder prevents repeated add statement "
    builder: list = []
    for unit, value in units.items():
        " Skip adding time if value of that time unit equals 0 "
        if value == 0:
            continue

        " Add value as string "
        builder.append(str(value))
        " If value is in plural, add 's' to the end"
        builder.append(unit if value <= 1 else f'{unit}s')

    " Convert builder to string literal with space between "
    message: str = ' '.join(builder)
    debug(f'Converted {seconds} seconds to {message}')

    return message
