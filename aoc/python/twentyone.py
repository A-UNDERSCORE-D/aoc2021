from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache as cache
import itertools

import sys
from typing import Counter
# sys.setrecursionlimit((1 << 15)-1)


@dataclass(frozen=True)
class Player:
    number: int
    position: int
    score: int = 0


def run_game(players: list[Player], max_score=1000, real_game=False) -> int:
    dice = 0
    while not any(p.score >= max_score for p in players):
        player = players[0]
        one = dice + 1
        two = dice + 2
        three = dice + 3
        dice += 3
        steps = one+two+three
        new_position = player.position + steps
        while new_position > 10:
            new_position -= 10

        new_score = player.score + new_position
        players[0] = Player(player.number, new_position, new_score)

        players[0], players[1] = players[1], players[0]

    loser, winner = players[0], players[1]
    assert winner.score > loser.score

    return loser.score * dice


def parse_input(input: str) -> list[Player]:
    lines = input.splitlines()

    one = lines[0].split()
    two = lines[1].split()
    return [Player(int(one[1]), int(one[-1])), Player(int(two[1]), int(two[-1]))]


def part_1(input: str) -> int:
    # [Player(1, 4), Player(2, 8)]
    players = parse_input(input)
    return run_game(players)

# inspired by reddit after looking at a few solutions etc.


@dataclass(frozen=True)
class State:
    positions: tuple[int, int]
    scores: tuple[int, int]

    def move(self, player: int, count: int) -> State:
        new_positions = list(self.positions)
        new_score = list(self.scores)
        new_positions[player] = (self.positions[player] + count - 1) % 10 + 1  # I hate these. black magic :P
        new_score[player] += new_positions[player]
        return State((new_positions[0], new_positions[1]), (new_score[0], new_score[1]))


possible_rolls_count = Counter((o+t+th for o in range(1, 4) for t in range(1, 4) for th in range(1, 4)))


@cache(maxsize=None)
def play(player: int, state: State) -> tuple[int, int]:
    if state.scores[0] >= 21:
        return 1, 0

    if state.scores[1] >= 21:
        return 0, 1

    next = 1 if player == 0 else 0
    result = (0, 0)

    for val, occ in possible_rolls_count.items():
        played = play(next, state.move(player, val))
        result = (result[0] + (played[0] * occ), result[1] + (played[1] * occ))

    return result


def part_2(input: str) -> int:
    players = parse_input(input)
    res = max(play(0, State((players[0].position, players[1].position), (0, 0))))
    print(play.cache_info())
    return res
