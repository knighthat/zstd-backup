from __future__ import annotations

from typing import Any, TypeVar

from src.logger import debug

T = TypeVar('T', bound=[str, int, float, bool, list, set, tuple, dict])


def verify(arg: Any, _type: T | tuple[T, ...], default: Any = None, force_cast: bool = False) -> T.__name__:
    """
    Attempt to verify the type of 'arg'.
    Type of 'arg' must be or included in '_type'.
    If '_type' does not contain type of 'arg',
    then 'default' value will be return if it's not None.
    'force_cast' will explicitly cast 'arg' to '_type'
    only when '_type' isn't a tuple and is eligible
    to be cast to said type.

    :param arg: value to check against
    :param _type:
        What type of 'arg' must be.
        Available types: str, int, float, bool, list, set, tuple, dict.
        It can also check against a tuple of types
        and return value if one of the types in the
        tuple matches the type of 'arg
    :param default:
        Fallback value in case 'arg''s type isn't match '_type'
    :param force_cast:
        Attempt to cast 'arg' to '_type' only when '_type' isn't a tuple

    :return: 'arg' if its type matches '_type' or 'default' if it's not None

    :raise TypeError:
        When '_type' doesn't contain type of 'arg' and 'default'
        is None or 'force_cast' isn't eligible when True
    """
    is_tuple: bool = isinstance(_type, tuple)
    if is_tuple:
        type_str: str = f'[{", ".join(t.__name__ for t in _type)}]'
    else:
        type_str: str = f'\'{_type.__name__}\''
    debug(f'Verifying type of \'{arg}\' against {type_str}')

    if not isinstance(arg, _type):

        if default is not None:
            debug(f'Default value of \'{default}\' of type \'{type(default).__name__}\' is returned in place of \'{arg}\' of type \'{type(arg).__name__}\'')
            return default

        if force_cast:
            if is_tuple:
                raise ValueError(f'\'_type\' must be a single type, not a tuple. Got {type_str}')

            debug(f'Attempting to force cast \'{arg}\' to {type_str}')
            return _type(arg)

        raise TypeError(f'{arg} is not an instance of type {type_str}')

    else:
        debug(f'\'{arg}\' matches type of {type_str}')
        return arg
