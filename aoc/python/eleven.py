from __future__ import annotations

from .util.direction import CARDINAL_DIAG
from copy import deepcopy


def p1_step(grid: list[list[int]]) -> tuple[list[list[int]], int]:
    flashed = []

    def flash(row: int, column: int):
        nonlocal flashed, grid
        if (row, column) in flashed:
            return
        flashed.append((row, column))

        for (nr, nc) in [(row+dr, column+dc) for (dc, dr) in CARDINAL_DIAG]:
            if nc < 0 or nc >= len(grid[0]) or nr < 0 or nr >= len(grid):
                continue

            grid[nr][nc] += 1

            if grid[nr][nc] > 9 and (nr, nc) not in flashed:
                flash(nr, nc)

    # increment everyone
    for row in range(len(grid)):
        for col in range(len(grid)):
            grid[row][col] += 1

    # check for flashes
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] > 9:
                flash(row, col)

    for (r, c) in flashed:
        grid[r][c] = 0

    return grid, len(flashed)


def highlight_num(n: int) -> str:
    if n > 9 or n == 0:
        return f'\033[1m{n}\033[m'

    return str(n)


def part_1(input: str) -> str:
    n_input = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
    grid: list[list[int]] = [[int(col) for col in row] for row in input.splitlines()]
    # new_grid: list[list[int]] = [[0 for _ in ]]

    total_flashes = 0
    for i in range(1, 101):
        grid, flashed = p1_step(grid)
        total_flashes += flashed
        # if i < 11 or i % 10 == 0:
        #     print(
        #         f'After Step {i} {flashed=} {total_flashes=}\n{chr(0x0A).join(" ".join(highlight_num(col) for col in row) for row in grid)}')

    return f'{total_flashes}'


def part_2(input: str) -> str:
    _input = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
    grid: list[list[int]] = [[int(col) for col in row] for row in input.splitlines()]
    # new_grid: list[list[int]] = [[0 for _ in ]]

    total_flashes = 0
    for i in range(1, 1024):
        grid, flashed = p1_step(grid)
        total_flashes += flashed

        all_flashed = flashed == sum(len(row) for row in grid)
        if all_flashed:
            return f'{i}'

    return f'{total_flashes}'
