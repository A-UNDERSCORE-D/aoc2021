from __future__ import annotations
from typing import TYPE_CHECKING

TEST_DATA = """2199943210
3987894921
9856789892
8767896789
9899965678"""

if TYPE_CHECKING:
    POINT = tuple[int, int]
    GRID = list[list[int]]


def parse_height_map(input: str) -> list[list[int]]:

    return [[int(c) for c in row] for row in input.split()]


def find_low_points(grid: list[list[int]]) -> list[tuple[int, int]]:
    low_points = []
    for y, row in enumerate(grid):
        for x, col in enumerate(row):

            if any(grid[ny][nx] <= col for nx, ny in safe_directions(grid, (x, y))):
                continue

            low_points.append((x, y))

    return low_points


def part_1(input: str) -> str:
    parsed = parse_height_map(input)

    low_points = find_low_points(parsed)

    count = sum([parsed[y][x] + 1 for (x, y) in low_points])

    return f"{count}"


def safe_directions(grid: list[list[int]], point: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = point
    x_len = len(grid[0])
    y_len = len(grid)
    out = []

    if (x - 1) >= 0:
        out.append((x-1, y))

    if (x + 1) < x_len:
        out.append((x+1, y))

    if (y - 1) >= 0:
        out.append((x, y-1))

    if (y + 1) < y_len:
        out.append((x, y+1))

    return out


def flood_fill_point(grid: list[list[int]], start_point: tuple[int, int], pretty=False, pretty_others: list[POINT] = None) -> list[POINT]:
    checked: list[POINT] = []
    to_check: list[POINT] = [start_point]
    to_print: list[POINT] = []

    while to_check:
        next = to_check.pop(0)
        checked.append(next)

        if pretty and pretty_others is not None:
            to_print.append(next)

        for p in safe_directions(grid, next):
            if p in checked:
                continue

            x, y = p
            if grid[y][x] == 9:
                continue

            to_check.append(p)

    if pretty and pretty_others is not None:
        import time
        for print_point in to_print:
            # for point in print_point:
            x, y = print_point
            col = grid[y][x]
            print(f'\033[{y+1};{x+10}H\033[1m{col}\033[m')
            time.sleep(0.001)

    return list(set(checked))


def print_basin(grid: GRID, basin: list[POINT], PRINT_BACKGROUNDS=False):
    to_print = []
    i = 0
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if (x, y) in basin:
                to_print.append(f'\033[{y+1};{x+10}H\033[1m{col}\033[m')

            elif PRINT_BACKGROUNDS:
                to_print.append(f'\033[{y+1};{x+10}H\033[40m.\033[m')

    print(''.join(to_print))


def part_2(input: str) -> str:
    import itertools
    import os

    # input = TEST_DATA
    parsed = parse_height_map(input)
    low_points = find_low_points(parsed)

    basins: list[list[POINT]] = []
    if os.getenv("VISUALIZE") is not None:
        print('\033c', end='')
        print(''.join(f'\033[{y+1};{x+10}H\033[40m.\033[m' for x in range(len(parsed[0])) for y in range(len(parsed))))
        import random
        random.shuffle(low_points)

    while low_points:
        if os.getenv('VISUALIZE') is not None:
            points = flood_fill_point(parsed, low_points.pop(0), pretty=True,
                                      pretty_others=list(itertools.chain.from_iterable(basins)))
        else:
            points = flood_fill_point(parsed, low_points.pop(0))
        low_points = [p for p in low_points if p not in points]
        basins.append(points)

    largest: list[int] = []
    for basin in basins:
        # print_basin(parsed, basin)
        if len(largest) < 3:
            largest.append(len(basin))
        else:
            largest.sort()
            for (i, other) in enumerate(largest):
                if len(basin) > other:
                    largest[i] = len(basin)
                    break

    return f'{largest[0] * largest[1] * largest[2]}'
