from __future__ import annotations
from dataclasses import dataclass


TEST_INPUT = "16,1,2,0,4,2,7,1,2,14"


@dataclass(frozen=True)
class CrabSub:
    position: int

    def fuel_to_move(self, target: int, exp=False) -> int:
        if not exp:
            return abs(self.position - target)

        steps = abs(self.position - target)
        return steps * (steps+1) // 2


def part_1(input: str) -> str:
    positions = [CrabSub(int(p)) for p in input.split(",")]

    best_fuel = -1

    for target in range(min(c.position for c in positions), max(c.position for c in positions)):
        fuel_required = sum(c.fuel_to_move(target) for c in positions)

        if fuel_required < best_fuel or best_fuel == -1:
            best_fuel = fuel_required

    return f"{best_fuel}"


def part_2(input: str) -> str:
    positions = [CrabSub(int(p)) for p in input.split(",")]

    best_fuel = -1

    for target in range(min(c.position for c in positions), max(c.position for c in positions)):
        fuel_required = sum(c.fuel_to_move(target, exp=True) for c in positions)

        if fuel_required < best_fuel or best_fuel == -1:
            best_fuel = fuel_required

    return f"{best_fuel}"
