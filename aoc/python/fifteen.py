from __future__ import annotations
from typing import TYPE_CHECKING

import heapq

from .util import direction

if TYPE_CHECKING:
    POINT = tuple[int, int]

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


def parse_graph(input: str) -> dict[POINT, int]:
    d = {}
    for row, r in enumerate(input.splitlines()):
        for col, c in enumerate(r):
            d[(row, col)] = int(c)

    return d


def dj(graph: dict[POINT, int], start: POINT, end: POINT):
    heap: list[tuple[int, POINT]] = []
    seen: set[POINT] = set()
    seen.add(start)

    def safe_dirs(s: POINT) -> list[POINT]:
        out = []
        for d in direction.CARDINAL:
            new_point = (s[0] + d[0], s[1]+d[1])

            if new_point in graph:
                out.append(new_point)

        return out

    heapq.heappush(heap, (0, start))

    i = 0
    while heap:
        i += 1
        if i % 30000 == 0:
            print(len(heap), len(seen))

        cost, point = heapq.heappop(heap)
        if point in seen and len(seen) > 1:
            continue

        seen.add(point)

        if point == end:
            return cost

        for dir in safe_dirs(point):
            if dir not in seen:
                heapq.heappush(heap, (cost+graph[dir], dir))

    return "?????"


def correct_add(a: int, b: int) -> int:
    out = a
    for _ in range(b):
        if out > 9:
            out = 1
        out += 1

    if out > 9:
        out = 1

    return out


def make_larger_graph(input: str) -> tuple[dict[POINT, int], POINT]:
    l = [[int(c) for c in r] for r in input.splitlines()]
    out_l: list[list[int]] = []

    for row in l:
        out_row: list[int] = []
        for i in range(5):
            out_row.extend(correct_add(c, i) for c in row)

        out_l.append(out_row)

    # okay, all 5 left to right done, now top to bottom
    start_len = len(out_l)
    for i in range(1, 5):
        for r_i in range(start_len):
            out_l.append([correct_add(c, i) for c in out_l[r_i]])

    out = {}

    for row_idx, r in enumerate(out_l):
        for col, c in enumerate(r):
            out[(row_idx, col)] = c

    L = out_l

    return (out, (len(out_l)-1, len(out_l[0])-1))


# from functools import ca


def cost_at(g: dict[POINT, int], max_row: int, max_col: int, row: int, col: int) -> int:
    original_coords = ((row % (max_row+1)), (col % (max_col+1)))

    off_row = row // (max_row+1)
    off_col = col // (max_col+1)
    original_cost = g[original_coords]

    cost = original_cost
    for i in range(max(off_row, off_col)):
        if cost == 9:
            cost = 1
        cost += 1

    return cost


def print_path(g: list[list[int]], p: list[POINT]):
    for row, l in enumerate(g):
        for col, n in enumerate(l):
            if (row, col) in p:
                print(f'\033[1m{n}\033[m', end='')

            else:
                print(n, end='')

        print()


def part_1(input: str) -> int | str:
    # input = TEST_DATA
    graph = parse_graph(input)

    return dj(graph, (0, 0), (len(input.splitlines())-1, len(input.splitlines()[0])-1))


def part_2(input: str) -> int | str:
    # input = TEST_DATA
    graph, end = make_larger_graph(input)

    return dj(graph, (0, 0), end)
