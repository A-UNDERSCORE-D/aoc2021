from __future__ import annotations
import traceback
# from . import one, two, three, four, five
from .util.human import time_call
from typing import Callable, List, TypeVar
import sys
import datetime

SHOW_TB = False


def make_dummy(error: str) -> tuple[TEST_FUNC, TEST_FUNC]:
    return (lambda _: error, lambda _: error)  # type: ignore


_T = TypeVar('_T')
TEST_FUNC = Callable[[str], _T]

TO_RUN: list[tuple[TEST_FUNC, TEST_FUNC]] = []
for n in (
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
    'seventeen', 'eighteen',
):
    to_set = None
    try:
        exec(f'from . import {n}', globals(), locals())
        mod = globals()[n]
        to_set = (mod.part_1, mod.part_2)

    except (ImportError, SyntaxError) as e:
        if SHOW_TB:
            traceback.print_exc()

        if isinstance(e, SyntaxError):
            msg = f'{e.msg}: {n}.py:{e.lineno}: {str(e.text).strip()}'
        else:
            msg = str(e)

        to_set = make_dummy(msg)

    TO_RUN.append(to_set)  # type: ignore


# TO_RUN: list[tuple[TEST_FUNC, TEST_FUNC]] = (
#     (one.part_1, one.part_2),  # type: ignore
#     (two.part_1, two.part_2),  # type: ignore
#     (three.part_1, three.part_2),  # type: ignore
#     (four.part_1, four.part_2),  # type: ignore
#     (five.part_1, five.part_2),  # type: ignore
# )


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
    from pathlib import Path
    requested = parse_args(sys.argv)
    input_dir = Path(__file__).parent.parent / 'input'

    for day in requested:
        if len(TO_RUN) <= day-1:
            print(f'Day {day:02}: Part 1: Not Found (0ns)')
            print(f'Day {day:02}: Part 2: Not Found (0ns)')
            print()
            continue

        p1, p2 = TO_RUN[day-1]

        with open(input_dir / f'{day:02}.input') as f:
            input = f.read()

        time, res = time_call(p1, input)
        print(f'Day {day:02}: Part 1: {res} ({time})')

        time, res = time_call(p2, input)
        print(f'Day {day:02}: Part 2: {res} ({time})')

        print()
