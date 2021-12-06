from __future__ import annotations
from typing import DefaultDict
TEST_CASE = "3,4,3,1,2"


def run_fish(fish: list[int], days: int) -> list[int]:
    for _ in range(days):
        current = len(fish)
        for i in range(current):
            f = fish[i]
            # no match because pypy testing helps here
            if f == 0:
                fish[i] = 6
                fish.append(8)

            else:
                fish[i] = f-1
    return fish


def part_1(input: str) -> int:
    # the dumb way
    # input = TEST_CASE
    fish: list[int] = list(map(int, input.split(",")))
    return smarter_way(fish, 80)


SHOW_PROGRESS_MOD = -1


def smarter_way(input_fish: list[int], days: int) -> int:
    fish: dict[int, int] = {i: 0 for i in range(9)}
    for f in input_fish:
        fish[f] += 1

    for iternum in range(days):
        # if SHOW_PROGRESS_MOD > 0 and iternum % SHOW_PROGRESS_MOD == 0:
        #     print(f'\rat {iternum}, {days - iternum} to go')
        new_fish = {i: 0 for i in range(9)}
        for day, count in fish.items():
            if day == 0:
                new_fish[6] += count
                new_fish[8] += count

            else:
                new_fish[day-1] += count
            # match day:
            #     case 0:
            #         new_fish[6] += count
            #         new_fish[8] += count
            #     case other:
            #         new_fish[other-1] += count

        fish = new_fish

    return sum(fish.values())
    ...


def part_2(input: str) -> int:
    fish: list[int] = list(map(int, input.split(",")))
    return smarter_way(fish, 256)


def bench() -> int:
    fish = list(map(int, TEST_CASE.split(',')))
    return smarter_way(fish, 9999999)


if __name__ == '__main__':
    # SHOW_PROGRESS_MOD = 10000
    from util.human import time_call, humanise_time

    time, num = time_call(bench)
    print(f'Bench took {time} and had result in ./out.nums')
    with open('./out.nums', 'w') as f:
        print(num, file=f)
