from __future__ import annotations
from dataclasses import dataclass
from typing import DefaultDict
TEST_INPUT = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def dot(self, other: Point) -> int:
        return (self.x * other.x) + (self.y * other.y)

    def wedge(self, other: Point) -> int:
        return (self.x * other.y) - (self.y * other.x)


def nicer_range(a, b) -> list[int]:
    if a > b:
        return list(range(a, b, -1))

    return list(range(a, b))


@dataclass
class LineSegment:
    start: Point
    end: Point

    def is_horiz_or_vert(self) -> bool:
        return self.start.x == self.end.x or self.start.y == self.end.y

    def is_fourty_five(self) -> bool:
        d = self.delta()
        return d.x == d.y

    def delta(self) -> Point:
        return Point(abs(self.start.x - self.end.x), abs(self.start.y - self.end.y))

    def slope(self) -> float:
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)

    def min(self) -> Point:
        return Point(min(self.start.x, self.end.x), min(self.start.y, self.end.y))

    def max(self) -> Point:
        return Point(max(self.start.x, self.end.x), max(self.start.y, self.end.y))

    def plot_straight_line(self) -> list[Point]:
        if self.start.x == self.end.x:
            return [Point(x=self.start.x, y=y) for y in range(self.min().y, (self.max().y + 1))]

        elif self.start.y == self.end.y:
            return [Point(x=x, y=self.start.y) for x in range(self.min().x, (self.max().x + 1))]

        elif self.is_fourty_five():
            return [Point(x, y) for x, y in zip(nicer_range(self.start.x, self.end.x), nicer_range(self.start.y, self.end.y))] + [self.end]

        else:
            raise ValueError(f'{self} is not a straight line')

    @staticmethod
    def from_str(line: str) -> LineSegment:
        start, end = line.split(' -> ')
        sX, sY = [int(x) for x in start.split(',')]
        eX, eY = [int(x) for x in end.split(',')]

        return LineSegment(Point(sX, sY), Point(eX, eY))


def part_1(input: str) -> int:
    lines: list[LineSegment] = [LineSegment.from_str(l) for l in input.splitlines()]
    lines = list(filter(lambda l: l.is_horiz_or_vert(), lines))

    hits: DefaultDict[Point, int] = DefaultDict(int)

    for line in lines:
        for point in line.plot_straight_line():
            hits[point] += 1

    overlaps = [1 for x in hits.values() if x > 1]

    return len(overlaps)


def part_2(input: str) -> int:
    # input = TEST_INPUT
    lines: list[LineSegment] = [LineSegment.from_str(l) for l in input.splitlines()]

    hits: DefaultDict[Point, int] = DefaultDict(int)

    for line in lines:
        for point in line.plot_straight_line():
            hits[point] += 1

    overlaps = [1 for x in hits.values() if x > 1]

    return len(overlaps)


if __name__ == '__main__':
    l = LineSegment.from_str('1,1 -> 5,5')
    print(l.slope())
