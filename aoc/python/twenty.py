from __future__ import annotations


def parse_input(input: str) -> tuple[str, dict[tuple[int, int], str]]:
    ehstr, imgstr = input.split('\n\n')
    ehstr = ''.join(ehstr.splitlines())  # just in case

    img = imgstr.splitlines()

    return ehstr, array_to_dict(img)


def make_coords(start_r: int, start_c: int):
    # our start is in the middle
    return [
        (start_r-1, start_c-1), (start_r-1, start_c), (start_r-1, start_c+1),
        (start_r, start_c-1), (start_r, start_c), (start_r, start_c+1),
        (start_r+1, start_c-1), (start_r+1, start_c), (start_r+1, start_c+1),
    ]


def print_image(i: dict[tuple[int, int], str], highlight: list[tuple[int, int]] | None = None, highlight_only: bool = False):
    max_r = max([c[0] for c in i])
    max_c = max([c[1] for c in i])
    if highlight is None:
        highlight = []
    else:
        print(highlight)
    for r in range(-2, max_r+3):
        for c in range(-2, max_c+3):
            to_print = i.get((r, c), '.')
            if (r, c) in highlight:
                print(f'\033[40m{to_print}\033[m', end='')
                continue

            print(to_print if not highlight_only else ' ', end='')

        print()

    print()


def array_to_dict(arr: list[list[str]] | list[str]) -> dict[tuple[int, int], str]:
    out = {}
    for r in range(len(arr)):
        for c in range(len(arr[0])):
            out[(r, c)] = arr[r][c]

    return out


def solve_1(eh: str, img: dict[tuple[int, int], str], not_found: str):
    max_r, min_r = max([c[0] for c in img]), min([c[0] for c in img])
    max_c, min_c = max([c[1] for c in img]), min([c[1] for c in img])

    new_img = []
    cur_row = []

    for r in range(-1, max_r+2):
        for c in range(-1, max_c+2):
            target_coords = make_coords(r, c)
            # given the input, if we're at iter 0, then everything is ., but at iter 1, everything is #
            # print_image(img, target_coords)

            values = ''.join(['1' if v == '#' else '0' for v in (
                img.get(x, not_found) for x in target_coords)])

            assert len(values) == 9
            # print(f'{(r, c)} -> {values} -- {int(values, 2)}')
            cur_row.append(eh[int(values, 2)])

        new_img.append(cur_row)
        cur_row = []

    n = array_to_dict(new_img)
    return n


def part_1(input: str) -> str:
    en, img = parse_input(input)
    from copy import deepcopy
    working_on = deepcopy(img)
    for i in (en[-1], en[0]):
        working_on = solve_1(en, working_on, i)

    return f'{sum(1 for k, v in working_on.items() if v == "#")}'


def part_2(input: str) -> str:
    en, img = parse_input(input)

    from copy import deepcopy
    working_on = deepcopy(img)
    blinky = [en[-1], en[0]] * 25
    assert len(blinky) == 50
    for i in blinky:
        working_on = solve_1(en, working_on, i)

    return f'{sum(1 for k, v in working_on.items() if v == "#")}'


TEST = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""
