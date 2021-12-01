import time

from util.lists import clump


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

if __name__ == '__main__':
    from util.human import humanise_time
    input = open("./aoc/input/01.input").read()
    t = time.monotonic_ns()
    res = part_1(input)
    end = time.monotonic_ns()
    print(f'Part 1: {res}, {humanise_time(end-t)}')

    t = time.monotonic_ns()
    res = part_2(input)
    end = time.monotonic_ns()
    print(f'Part 2: {res}, {humanise_time(end-t)}')
