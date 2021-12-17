from __future__ import annotations
from typing import cast


def sign(n: int) -> int:
    if n > 0:
        return 1

    elif n < 0:
        return -1

    return 0


def toward_zero(n: int, delta: int = 1) -> int:
    if n == 0:
        return n
    elif n > 0:
        return n - delta

    return n + delta


def simulate(start: tuple[int, int], velocity_start: tuple[int, int], x_area: list[int], y_area: list[int]) -> tuple[list[tuple[int, int]], bool]:
    xpos, ypos = start
    xvel, yvel = velocity_start

    # xmin, xmax = x_area
    # ymin, ymax = y_area

    # xa = list(range(min(x_area), max(x_area))) + [max(x_area)]
    # ya = list(range(min(y_area), max(y_area))) + [max(y_area)]

    # print(xa)
    # print(ya)
    positions = []

    while True:
        xpos += xvel
        ypos += yvel

        xvel = toward_zero(xvel)
        yvel -= 1
        # print(f'{(xpos, ypos)=} {(xvel, yvel)=} {x_area=}, {y_area=}')

        positions.append((xpos, ypos))

        if xpos in x_area and ypos in y_area:
            # print(f"{(xpos, ypos)=} {(xvel, yvel)=} in area")
            return positions, True

        if xvel == 0 and xpos not in x_area:
            # print("impossible")
            return positions, False

        if ypos < min(y_area):
            # print("passed Y")
            return positions, False


def part_1(input: str) -> str:
    # input = 'target area: x=20..30, y=-10..-5'
    target_range = input.split(': ')[1]
    xrange_s, yrange_s = target_range.split(', ')

    xrange_s, yrange_s = xrange_s.split('=')[1], yrange_s.split('=')[1]

    xrange: tuple[int, int] = cast('tuple[int, int]', tuple(int(x) for x in xrange_s.split('..')))
    yrange: tuple[int, int] = cast('tuple[int, int]', tuple(int(x) for x in yrange_s.split('..')))

    # okay, we always need to go in the x direction of the target area

    xvel = 1
    best_height = -1e50

    x_range = list(range(min(xrange), max(xrange))) + [max(xrange)]
    y_range = list(range(min(yrange), max(yrange))) + [max(yrange)]

    for x in range(0, max(xrange)+1):
        for y in range(0, 100):
            positions, ok = simulate((0, 0), (x, y), x_range, y_range)
            if not ok:
                continue

            max_y = max(p[1] for p in positions)
            if max_y > best_height:
                best_height = max_y

    return f'{best_height}'


def part_2(input: str) -> str:
    target_range = input.split(': ')[1]
    xrange_s, yrange_s = target_range.split(', ')

    xrange_s, yrange_s = xrange_s.split('=')[1], yrange_s.split('=')[1]

    xrange: tuple[int, int] = cast('tuple[int, int]', tuple(int(x) for x in xrange_s.split('..')))
    yrange: tuple[int, int] = cast('tuple[int, int]', tuple(int(x) for x in yrange_s.split('..')))

    x_range = list(range(min(xrange), max(xrange))) + [max(xrange)]
    y_range = list(range(min(yrange), max(yrange))) + [max(yrange)]

    vels = []
    for x in range(0, max(xrange)+1):
        for y in range(min(yrange), max(yrange)+150):
            positions, ok = simulate((0, 0), (x, y), x_range, y_range)
            if not ok:
                continue

            vels.append((x, y))

    return f'{len(vels)}'
