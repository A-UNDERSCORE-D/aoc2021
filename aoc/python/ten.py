from __future__ import annotations
from collections import deque

OPENS = "([{<"
CLOSES = ")]}>"

LUT = {
    ')': '(',
    '}': '{',
    '>': '<',
    ']': '[',

    '(': ')',
    '{': '}',
    '<': '>',
    '[': ']',
}
POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

TEST_INPUT = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


def is_valid(line: str) -> tuple[bool, str, int]:
    queue: deque[str] = deque()

    for i, c in enumerate(line):
        # print(f'{line} -> {line[i:]:>25} {queue=}')
        if c in OPENS:
            queue.append(c)
        elif c in CLOSES:
            last_open = queue.pop()
            # print(last_open)
            if LUT[c] != last_open:
                return False, c, i

    return True, "".join(queue), -1


def part_1(input: str) -> str:
    # input = TEST_INPUT
    total = 0
    for line in input.splitlines():
        ok, invalid_char, pos = is_valid(line)

        # print(f'{line!r}\t{ok=} {invalid_char=} {pos=}')
        # print(f'{" " * (pos + 1)}^')

        if ok:
            continue

        total += POINTS[invalid_char]

    return f"{total}"


P2_POINTS = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def part_2(input: str) -> str:
    # input = TEST_INPUT
    scores = []
    for line in input.splitlines():
        valid, result, _ = is_valid(line)
        if not valid:
            continue

        line_score = 0
        to_complete = list(map(lambda c: LUT[c], result[::-1]))
        for c in to_complete:
            line_score *= 5
            line_score += P2_POINTS[c]

        scores.append(line_score)

    scores.sort()
    x = scores[len(scores) // 2]

    return f'{x}'
