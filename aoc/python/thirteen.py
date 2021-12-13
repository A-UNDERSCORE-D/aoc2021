from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass
from copy import deepcopy
import itertools
if TYPE_CHECKING:
    GRID = list[list[bool]]

TEST_INPUT = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""


@dataclass
class Fold:
    position: int
    along_x: bool


def parse_input(input: str) -> tuple[GRID, list[Fold]]:
    p_str, ins_str = input.split("\n\n")

    instructions = [Fold(int(num), loc == 'x') for (loc, num) in map(
        lambda s: s.split(" ")[2].split("="), ins_str.splitlines())]

    points = [(int(x), int(y)) for x, y in map(lambda s: s.split(","), p_str.splitlines())]

    maxX = max(x for x, _ in points)
    maxY = max(y for _, y in points)

    grid = []

    for i in range(maxY+1):
        grid.append([False]*(maxX+1))

    for col, row in points:
        grid[row][col] = 1

    return (grid, instructions)


NUMS = {0: '.', 1: '#'}


def print_grid(g: GRID):
    for row in g:
        print(''.join(NUMS[x] if x in NUMS else str(x) for x in row))


def fold_grid(g: GRID, instruction: Fold) -> GRID:
    to_fold = g
    if instruction.along_x:
        left, right = (
            [r[:instruction.position] for r in to_fold],
            [r[instruction.position+1:] for r in to_fold]
        )

        for r in right:
            r.reverse()

        for row in range(len(right)):
            for col in range(len(right[row])):
                left[row][col] |= right[row][col]

        to_fold = left

    else:
        top, bottom = to_fold[:instruction.position], to_fold[instruction.position+1:]
        bottom.reverse()

        for row in range(len(bottom)):
            for col in range(len(bottom[row])):
                top[row][col] |= bottom[row][col]

        to_fold = top

    return to_fold


def part_1(input: str) -> str:
    g, i = parse_input(input)
    g = fold_grid(g, i[0])

    return f'{sum(itertools.chain.from_iterable(g))}'


def part_2(input: str) -> str:
    g, i = parse_input(input)

    for instruction in i:
        g = fold_grid(g, instruction)

    print_grid(g)

    return 'see above'
