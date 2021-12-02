from . import one, two
from .util.human import time_call
from typing import List
import sys

import datetime
TO_RUN = (
    (one.part_1, one.part_2),
    (two.part_1, two.part_2),
)


def december_day() -> bool:

    now = datetime.datetime.now()
    return now.day <= 25 and now.month == 12


def parse_args(args: List[str]) -> List[int]:
    if 'all' in args or (len(args) == 1 and not december_day()):
        return list(range(1, 26))

    if len(args) > 1:
        return [int(a) for a in args if a.isnumeric()]

    if december_day():
        return [datetime.datetime.now().day]

    return list(range(1, 26))


if __name__ == '__main__':

    requested = parse_args(sys.argv)

    for day in requested:
        if len(TO_RUN) <= day-1:
            print(f'Day {day:02}: Part 1: Not Found (0ns)')
            print(f'Day {day:02}: Part 2: Not Found (0ns)')
            print()
            continue

        p1, p2 = TO_RUN[day-1]
        with open(f'input/{day:02}.input') as f:
            input = f.read()

        time, res = time_call(p1, input)
        print(f'Day {day:02}: Part 1: {res} ({time})')

        time, res = time_call(p2, input)
        print(f'Day {day:02}: Part 2: {res} ({time})')

        print()
