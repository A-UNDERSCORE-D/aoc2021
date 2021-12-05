from __future__ import annotations
from .util.lists import clump


def part_1(input: str) -> str:
    ints = [int(s) for s in input.splitlines()]

    last = ints[0]
    count = 0
    for i in ints[1:]:
        if i > last:
            count += 1

        last = i

    return str(count)


def part_2(input: str) -> str:
    ints = [int(s) for s in input.splitlines()]
    windows = list(clump(ints, 3))

    s = sum(windows[0])
    c = 0
    for w in windows[1:]:
        w_sum = sum(w)
        if w_sum > s:
            c += 1

        s = w_sum

    return str(c)


example = """199
200
208
210
200
207
240
269
260
263"""


def run():
    from .util.human import time_call
    input = open("input/01.input").read()

    time, res = time_call(part_1, input)
    print(f'Day 01: Part 1: {res} ({time})')

    time, res = time_call(part_2, input)
    print(f'Day 01: Part 2: {res} ({time})')


if __name__ == '__main__':
    run()
