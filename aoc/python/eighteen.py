from __future__ import annotations
from typing import Any
import math
from copy import deepcopy


def parse_input(input: str) -> list[Any]:
    out = []

    for line in input.splitlines():
        # cheating? nah
        out.append(eval(line))

    return out


def flatten_input_paths(input: list[Any], current_path: list[int] | None = None) -> tuple[list[int], list[list[int]]]:
    flat = []
    paths = []
    if current_path is None:
        current_path = []

    for i, pair_item in enumerate(input):
        new_path = current_path + [i]
        if isinstance(pair_item, list):
            nf, np = flatten_input_paths(pair_item, new_path)
            flat += nf
            paths += np

        else:
            flat.append(pair_item)
            paths.append(current_path)

    return flat, paths


def split_on_first_depth_four_pair(nums: list[int], paths: list[list[int]]):
    flat_out = []
    depths_out = []
    first_four = []
    four_c = 0
    for (i, p) in enumerate(paths):
        if len(p) == 4:
            first_four.append(nums[i])
            four_c += 1

        if four_c == 2:
            flat_out.append(nums[:i-1])
            flat_out.append(nums[i+1:])
            depths_out.append(paths[:i-1])
            depths_out.append(paths[i+1:])
            break

    return flat_out, first_four, depths_out


def explode_pair(lst: list[Any]) -> bool:
    flat, paths = flatten_input_paths(lst)
    if not any(len(n) >= 4 for n in paths):
        return False

    (flat_l, flat_r), to_explode, (depths_l, depths_r) = split_on_first_depth_four_pair(flat, paths)
    new_left, new_right = -1, -1

    if len(flat_l) > 0:
        new_left = flat_l[-1] + to_explode[0]

    if len(flat_r) > 0:
        new_right = flat_r[0] + to_explode[1]

    if new_left != -1:
        # new_left
        c = lst
        for p in depths_l[-1]:
            c = c[p]

        # c is now 1 above the target, if the right most is a list, we want to set the left
        if isinstance(c[1], int):
            assert c[1] == flat_l[-1], (c[1], flat_l[-1])
            c[1] = new_left
        else:
            assert c[0] == flat_l[-1], (c[0], flat_l[-1])
            c[0] = new_left

    if new_right != -1:
        c = lst
        for p in depths_r[0]:
            c = c[p]

        # c is now 1 above the target, we want to set the left most value we can
        if isinstance(c[0], int):
            assert c[0] == flat_r[0], (c[0], flat_r[0])
            c[0] = new_right

        else:
            assert c[1] == flat_r[0], (c[1], flat_r[0])
            c[1] = new_right

    # the last step is to zero out the pair. which we can do by finding the first length four path

    path = []
    for p in paths:
        if len(p) == 4:
            path = p[:-1]
            break

    c = lst
    for p in path:
        c = c[p]

    if isinstance(c[0], list):
        c[0] = 0

    elif isinstance(c[1], list):
        c[1] = 0

    else:
        raise ValueError('wtf?')

    return True


def split(lst: list[Any]) -> bool:
    flat, paths = flatten_input_paths(lst)
    target = []
    target_idx = -1
    target_num = -1
    for (i, (num, path)) in enumerate(zip(flat, paths)):
        if num >= 10:
            target = path
            target_idx = i
            target_num = num
            break

    # print(target, target_idx, target_num)
    if target_idx == -1:
        return False

    new = [math.floor(target_num / 2.0), math.ceil(target_num / 2.0)]
    # print(f'{target_num} -> {new}')

    c = lst
    for p in target:
        c = c[p]

    if c[0] == target_num:
        c[0] = new

    elif c[1] == target_num:
        c[1] = new

    else:
        raise ValueError('wat')
    return True


def reduce_sailfish(numbers: list[Any]) -> bool:
    # we need to reduce, start with pairs
    if explode_pair(numbers):
        # print('e: ', numbers)
        return True

    elif split(numbers):
        # print('s: ', numbers)
        return True

    return False


def add(left: list[Any], right: list[Any]) -> list[Any]:

    new = [deepcopy(left), deepcopy(right)]
    # print('a: ', new)
    while True:
        did_something = reduce_sailfish(new)
        # print(did_something)

        if not did_something:
            break

    return new


def magnitude(x: list[Any] | int) -> int:
    if isinstance(x, int):
        return x

    return (magnitude(x[0]) * 3) + (magnitude(x[1]) * 2)


def part_1(input: str) -> str:
    parsed = parse_input(input)
    current = parsed[0]

    for n in parsed[1:]:
        current = add(current, n)

    return f'{magnitude(current)}'


def part_2(input: str) -> str:
    best_mag = 0
    parsed = parse_input(input)

    for x in parsed:
        for y in parsed:
            m = magnitude(add(x, y))

            if m > best_mag:
                best_mag = m

    return f'{best_mag}'
