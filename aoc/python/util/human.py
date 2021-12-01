from typing import Callable, Tuple, TypeVar
import time


NANOSECOND = 1
MICROSECOND = NANOSECOND * 1000
MILLISECOND = MICROSECOND * 1000
SECOND = MILLISECOND * 1000
MINUTE = SECOND * 60
HOUR = MINUTE * 60
DAY = HOUR * 24


TIME_LUT = {
    DAY:            'd',
    HOUR:           'h',
    MINUTE:         'm',
    SECOND:         's',
    MILLISECOND:    'ms',
    MICROSECOND:    'µs',
    NANOSECOND:     'ns',
}


def _ifexists(i: float, d: str) -> str:
    if i > 0:
        return f'{i}{d}'

    return ''


def humanise_time(nanos: int) -> str:
    time = ''

    for division, name in TIME_LUT.items():
        n, remainder = divmod(nanos, division)
        if n > 0 and n - 1 > 0.001:
            time += f'{n}.{remainder}{name}'
            break

        nanos = remainder

    return time.strip()


_T = TypeVar('_T')


def time_call(f: Callable[..., _T], *args, **kwargs) -> Tuple[str, _T]:  # type: ignore
    start = time.monotonic_ns()
    res = f(*args, **kwargs)
    end = time.monotonic_ns()

    return (humanise_time(end - start), res)


if __name__ == '__main__':
    print(humanise_time(1337654654))
