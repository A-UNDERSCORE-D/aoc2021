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
    MILLISECOND:     'ms',
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
            time += f'{n}{name}'

        nanos = remainder

    return time


if __name__ == '__main__':
    print(humanise_time(1337654654))
