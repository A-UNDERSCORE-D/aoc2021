from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .util import direction

if TYPE_CHECKING:
    GRID = list[list[int]]

TEST_DATA = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


def parse(input: str) -> GRID:
    return [[int(c) for c in row] for row in input.splitlines()]


@dataclass(frozen=True)
class DirEntry:
    position: tuple[int, int]
    weight: int

    def __repr__(self) -> str:
        return f'({self.position[0]}, {self.position[1]})'


def safe_directions(g: GRID, start: DirEntry, diagonal=False) -> list[DirEntry]:
    out = []

    start_row, start_col = start.position
    for d in direction.CARDINAL:
        delta_row, delta_col = d

        row = start_row + delta_row
        col = start_col + delta_col
        if row >= len(g) or row < 0:
            continue

        if col >= len(g[0]) or col < 0:
            continue

        out.append(DirEntry((row, col), g[row][col]))

    return out


BEST_PATH_SCORE = 1e10
TOTAL_CALLS = 0

"""
Cache by:
    storing the best path from a given position to the target
    checking if we have a cached route from a given position to the target
"""
CACHE: dict[DirEntry, tuple[list[DirEntry], int]] = {}


def recurse_dj(g: GRID, current_path: list[DirEntry], current_weight, current_node: DirEntry, target_position: DirEntry, depth: int) -> tuple[list[DirEntry], int]:
    global BEST_PATH_SCORE, TOTAL_CALLS
    TOTAL_CALLS += 1
    path = current_path + [current_node]

    dirs_to_check = safe_directions(g, current_node)
    path_sum = current_weight + current_node.weight

    # dirs_to_check.sort(key=lambda d: d.weight)
    dirs_to_check.sort(key=lambda d: d.position, reverse=True)  # prefer down and right

    results: list[tuple[list[DirEntry], int]] = []
    for d in dirs_to_check:
        if d in path:
            # we've been here! skip!
            continue

        if d == target_position:
            # base case, found the bottom
            results.append((path + [d], path_sum + d.weight))
            continue

        if not path_sum + d.weight < BEST_PATH_SCORE:
            # going this way doesnt help us
            continue

        # we didnt find the target, keep going down
        r = recurse_dj(g, path, path_sum, d, target_position, depth+1)
        if r[1] == -1:
            continue

        results.append(r)

    # results = [r for r in results if r[0]]

    if not results:
        return [], -1

    best_result = sorted(results, key=lambda r: r[1])[0]
    if not best_result:
        return [], -1

    if best_result[1] <= BEST_PATH_SCORE and best_result[1] > 0:
        # print(f'{best_result[1]} <= {BEST_PATH_SCORE} [{depth}]')
        BEST_PATH_SCORE = best_result[1]
        return best_result

    return [], -1


def print_path(g: GRID, p: list[DirEntry]):
    for row, l in enumerate(g):
        for col, n in enumerate(l):
            if DirEntry((row, col), n) in p:
                print(f'\033[1m{n}\033[m', end='')

            else:
                print(n, end='')

        print()


def part_1(input: str) -> str:
    # input = TEST_DATA
    parsed = parse(input)
    print(len(parsed), len(parsed[0]))
    # compute A score that is something to start with so the algo goes a bit faster:
    start_path = []
    for row in range(len(parsed)):
        start_path.append(DirEntry((row, row), parsed[row][row]))

    # for col in range(1, len(parsed[0])):
    #     start_path.append(DirEntry((len(parsed)-1, col), parsed[-1][col]))

    print_path(parsed, start_path)
    assert len(set(start_path)) == len(start_path)
    global BEST_PATH_SCORE
    BEST_PATH_SCORE = sum(n.weight for n in start_path[1:])

    start = DirEntry((0, 0), parsed[0][0])
    end = DirEntry((len(parsed)-1, len(parsed[0])-1), parsed[-1][-1])

    # result = recurse_dj(parsed, [], -end.weight, end, start, 0)
    result = recurse_dj(parsed, [], -start.weight, start, end, 0)
    s = result[1]
    print(result)
    # print(s)

    print_path(parsed, result[0])

    return f'{s} -- {TOTAL_CALLS}'


def part_2(input: str) -> str:
    return ''
