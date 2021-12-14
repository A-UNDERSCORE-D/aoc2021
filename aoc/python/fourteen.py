from __future__ import annotations

from collections import Counter, deque


TEST_INPUT = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


def parse_input(input: str) -> tuple[str, dict[str, str]]:
    lines = input.splitlines()
    rules = {}

    for line in lines[2:]:
        k, v = line.split(' -> ')
        rules[k] = v

    return (lines[0], rules)


def step(template: list[str], rules: dict[str, str]) -> list[str]:
    new_template: deque[str] = deque()
    for (i, first) in enumerate(template):
        second = template[i+1] if i + 1 < len(template) else ''
        joined = first+second

        new_template.append(first)
        if joined in rules:
            new_template.append(rules[joined])

    # print(new_template)
    return list(new_template)


def count(s: str, target: str):
    return sum(1 for i in range(len(s)) if s[i:].startswith(target))


def part_1(input: str) -> str:
    template, rules = parse_input(input)
    template_l = list(template)
    for _ in range(10):
        template_l = step(template_l, rules)

    c = Counter(template_l).most_common()
    return f'{c[0][1]-c[-1][1]}'


def part_2(input: str) -> str:
    # This solution is inspired by https://www.reddit.com/r/adventofcode/comments/rfzq6f/2021_day_14_solutions/hohetkp/
    template, rules = parse_input(input)
    pair = {p: count(template, p) for p in rules}
    # result pair -> source pair, ie, the count of result goes up by 1 for every source in the current template
    roots: dict[str, list[str]] = {p: [] for p in rules}

    for (source, insert) in rules.items():
        roots[source[0]+insert].append(source)
        roots[insert+source[1]].append(source)

    def generate(frequencies: dict[str, int], n: int) -> list[int]:
        new_frequencies = frequencies.copy()
        for _ in range(n):
            # do the math to update frequencies to the final value
            # that is, the frequency of its current value is equal to the sum of its sources
            # so, for every X, Y, and Z there is, there is Z number of As, where Z is the sum of the counts
            new_frequencies = {p: sum(new_frequencies[source] for source in roots[p]) for p in rules}

        # this is the count of *characters*
        count = {e: 0 for p in rules for e in p}

        for pair, freq in new_frequencies.items():
            count[pair[0]] += freq
            count[pair[1]] += freq

        #
        count[template[0]] += 1
        count[template[-1]] += 1
        # numbers are counted twice because of the sliding window
        return [v // 2 for v in count.values()]

    res = generate(pair, 40)

    return f'{max(res) - min(res)}'
