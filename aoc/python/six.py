from __future__ import annotations
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
    fish: list[int] = [0 for _ in range(9)]
    for f in input_fish:
        fish[f] += 1

    for iternum in range(days):
        if SHOW_PROGRESS_MOD > 0 and iternum % SHOW_PROGRESS_MOD == 0:
            print(f'\rat {iternum}, {days - iternum} to go')
        new_fish = [0 for _ in range(9)]
        for day, count in enumerate(fish):
            if day == 0:
                new_fish[6] += count
                new_fish[8] += count

            else:
                new_fish[day-1] += count

        fish = new_fish

    return sum(fish)


def part_2(input: str) -> int:
    fish: list[int] = list(map(int, input.split(",")))
    return smarter_way(fish, 256)


def bench() -> int:
    fish = list(map(int, TEST_CASE.split(',')))
    return smarter_way(fish, 2**26)


if __name__ == '__main__':
    SHOW_PROGRESS_MOD = 100000
    from util.human import time_call, humanise_time

    time, num = time_call(bench)
    print(f'Bench took {time} and had result in ./out.nums')
    with open('./out.nums', 'w') as f:
        print(num, file=f)
