from collections import defaultdict


def part_1(input: str) -> str:

    zeros = defaultdict(int)
    ones = defaultdict(int)

    for line in input.splitlines():
        for i, c in enumerate(line):
            match c:
                case "0":
                    zeros[i] += 1
                case "1":
                    ones[i] += 1

    gamma = ""
    epsilon = ""

    for i in range(len(input.splitlines()[0])):
        if zeros[i] > ones[i]:
            gamma += '0'
            epsilon += '1'

        else:
            gamma += '1'
            epsilon += '0'

    gamma, epsilon = int(gamma, 2), int(epsilon, 2)

    return str(gamma * epsilon)


def most_common_bit(binary: list[str], n=0) -> str | None:
    ones, zeros = 0, 0
    for line in binary:
        if line[n] == '1':
            ones += 1
        else:
            zeros += 1

    if ones == zeros:
        return None

    elif ones > zeros:
        return '1'

    return '0'


def filter_bits(numbers: list[str], most_common=True):  # isnt that fun?
    for i in range(len(numbers[0])):
        mc = most_common_bit(numbers, i)
        if mc is None:
            mc = '1'

        if not most_common:
            if mc == '1':
                mc = '0'

            else:
                mc = '1'

        new_numbers = [n for n in numbers if n[i] == mc]
        if len(new_numbers) == 0:
            break

        numbers = new_numbers

    assert len(numbers) == 1, f'{numbers=}'
    return numbers[0]


def part_2(input: str) -> str:
    split = input.split()
    ox = int(filter_bits(split), 2)
    scrub = int(filter_bits(split, False), 2)
    return f'{ox * scrub}'
