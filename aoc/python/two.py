from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Submarine:
    x: int = 0
    aim: int = 0
    depth: int = 0

    def move(self, instruction: str, p2: bool):
        split = instruction.split(" ")
        match (split[0], int(split[1])):
            case ("forward", x):
                self.x += x
                if p2:
                    self.depth += self.aim * x
            case ("up", x):
                if p2:
                    self.aim -= x

                else:
                    self.depth -= x

            case ("down", x):
                if p2:
                    self.aim += x

                else:
                    self.depth += x

            case (a, b):
                print(f"Unknown instruction {a} {b}")


def part_1(input: str) -> str:
    sub = Submarine()
    for instruction in input.splitlines():
        sub.move(instruction, False)

    return str(sub.x * sub.depth)


def part_2(input: str) -> str:
    sub = Submarine()
    for instruction in input.splitlines():
        sub.move(instruction, True)

    return str(sub.x * sub.depth)
