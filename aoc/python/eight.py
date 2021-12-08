from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, DefaultDict, TypeVar, cast
import itertools
KNOWN_LENGTHS = {
    1: 2,
    4: 4,
    7: 3,
    8: 7,
}

_K = TypeVar('_K')
_V = TypeVar('_V')


def reverse_lookup(d: dict[_K, _V], value: _V) -> _K | None:
    for k, v in d.items():
        if v == value:
            return k

    return None


if TYPE_CHECKING:
    RAW_DIGIT = list[bool]


@dataclass
class Digit:
    number: int
    raw_mapping: RAW_DIGIT
    char_mapping: str | None = None

    def shared_faces(self, other) -> list[bool]:
        return [x == y and x for (x, y) in zip(self.raw_mapping, other.raw_mapping)]

    def __and__(self, __t: Digit) -> RAW_DIGIT:
        return self.shared_faces(__t)

    def with_mapping(self, mapping: str) -> Digit:
        return Digit(self.number, self.raw_mapping.copy(), mapping)

    def important_mapped_chars(self) -> list[str]:
        if self.char_mapping is None:
            raise ValueError

        return [s for (s, b) in zip(self.char_mapping, self.raw_mapping) if b]

    def str_rep(self):
        return "".join([c for (i, c) in enumerate('abcdefg') if self.raw_mapping[i]])

    def mapped_str_rep(self):
        assert self.char_mapping is not None
        return "".join([c for (i, c) in enumerate(self.char_mapping) if self.raw_mapping[i]])


# These map to:
#    0000
#   1    2
#   1    2
#    3333
#   4    5
#   4    5
#    6666
DIGITS = [
    Digit(0, [True, True, True, False, True, True, True]),       # 0
    Digit(1, [False, False, True, False, False, True, False]),   # 1
    Digit(2, [True, False, True, True, True, False, True]),      # 2
    Digit(3, [True, False, True, True, False, True, True]),      # 3
    Digit(4, [False, True, True, True, False, True, False]),     # 4
    Digit(5, [True, True, False, True, False, True, True]),      # 5
    Digit(6, [True, True, False, True, True, True, True]),       # 6
    Digit(7, [True, False, True, False, False, True, False]),    # 7
    Digit(8, [True, True, True, True, True, True, True, True]),  # 8
    Digit(9, [True, True, True, True, False, True, True]),       # 9
]

assert(len(l.raw_mapping) == 7 for l in DIGITS)


def print_digit(d: list[bool]):
    def dot_or(idx: int) -> str:
        if d[idx]:
            return 'abcdefg'[idx]

        return '.'

    print(f'''
     {dot_or(0)}{dot_or(0)}{dot_or(0)}{dot_or(0)}
    {dot_or(1)}    {dot_or(2)}
    {dot_or(1)}    {dot_or(2)}
     {dot_or(3)}{dot_or(3)}{dot_or(3)}{dot_or(3)}
    {dot_or(4)}    {dot_or(5)}
    {dot_or(4)}    {dot_or(5)}
     {dot_or(6)}{dot_or(6)}{dot_or(6)}{dot_or(6)}
    ''')


if __name__ == '__main__':
    for (i, d) in enumerate(DIGITS):
        print(i)
        print_digit(d.raw_mapping)
        print(d.str_rep())
        print()


TEST_INPUT = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


def parse_input(i: str) -> list[tuple[list[str], list[str]]]:
    out = []
    for line in i.splitlines():
        inputs_s, outputs_s = line.split(" | ")
        inputs = inputs_s.split()
        outputs = outputs_s.split()

        out.append((inputs, outputs))

    return out


def part_1(input: str) -> int:
    # input = TEST_INPUT
    parsed = [FourDigitSegment(inp, out) for (inp, out) in parse_input(input)]
    return sum(p.part_1() for p in parsed)


@dataclass
class FourDigitSegment:
    inputs: list[str]
    outputs: list[str]
    _ordered_inputs: dict[int, list[str]] | None = None

    def part_1(self) -> int:
        return len([True for x in self.outputs if len(x) in KNOWN_LENGTHS.values()])

    @property
    def ordered_inputs(self) -> dict[int, list[str]]:
        if self._ordered_inputs is not None:
            return self._ordered_inputs

        x = DefaultDict(list)

        for i in self.inputs:
            x[len(i)].append(i)

        return dict(x)

    def brute_resolve(self) -> str:
        all_options: set[str] = set()
        for v in self.inputs:
            all_options |= set(v)

        assert len(all_options) == 7, all_options
        valids: list[str] = []
        for option in itertools.permutations(list(all_options)):
            if not self.test_brute(list(option)):
                continue

            valids.append(''.join(option))

        assert len(valids) == 1
        return valids[0]

    def test_brute(self, chars: list[str]) -> bool:
        """
        Given a list of signals
        we need to check that the signals we expect appear we we expect them to. eg signals for 1 need to appear in
        inputs of length 2, and so on
        """

        """
         aaa
        b   c
        b   c 
         ddd
        e   f
        e   f
         ggg
        """
        char_mapping = {a: n for (a, n) in zip('abcdefg', chars)}

        first_stage = all((
            # 1
            char_mapping['c'] in self.ordered_inputs[2][0],
            char_mapping['f'] in self.ordered_inputs[2][0],

            # 4
            char_mapping['b'] in self.ordered_inputs[4][0],
            char_mapping['c'] in self.ordered_inputs[4][0],
            char_mapping['d'] in self.ordered_inputs[4][0],
            char_mapping['f'] in self.ordered_inputs[4][0],

            # 7
            char_mapping['a'] in self.ordered_inputs[3][0],
            char_mapping['c'] in self.ordered_inputs[3][0],
            char_mapping['f'] in self.ordered_inputs[3][0],
        ))

        if not first_stage:
            return False

        # so now we know the ones that this is at least somewhat valid.
        # Now to find the numbers we cant just get at via ... reduction is a bad word but sure

        # for zero, there must be at least one imput of length 6 with a, b, c, e, f, g

        sixes = self.ordered_inputs[6].copy()

        for to_check in ('abcefg', 'abdefg', 'abcdfg'):
            to_remove = None

            for possible in sixes:
                if not all(char_mapping[c] in possible for c in to_check):
                    continue

                if to_remove != None:
                    print(to_remove, possible, "???")

                to_remove = possible

            if to_remove is None:
                return False

        # we have a valid 6, 9, and 0
        # now, we have found: 0 1     4   6 7   9
        # so we need        :     2 3   5
        # (we dont need 8, its free)

        # so we do so again, but with fives not sixes
        fives = self.ordered_inputs[5].copy()
        for to_check in ('acdeg', 'acdfg', 'abdfg'):
            to_remove = None
            for possible in fives:
                if not all(char_mapping[c] in possible for c in to_check):
                    continue

                if to_remove != None:
                    print(to_remove, possible, "???")

                to_remove = possible

            if to_remove is None:
                return False

        return True

    def outputs_given(self, mapping: str) -> list[Digit]:
        out = []
        for output in self.outputs:
            for digit in [d.with_mapping(mapping) for d in DIGITS]:
                if set(digit.mapped_str_rep()) == set(output):
                    out.append(digit)

        return out

    def part_2(self):
        return int(''.join([str(d.number) for d in self.outputs_given(self.brute_resolve())]))


def part_2(input: str) -> int:
    parsed = [FourDigitSegment(inp, out) for (inp, out) in parse_input(input)]
    return sum(e.part_2() for e in parsed)
