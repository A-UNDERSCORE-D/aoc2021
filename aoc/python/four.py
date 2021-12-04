from dataclasses import dataclass, field
import itertools


@dataclass
class BoardNumber:
    n: int
    marked: bool = False

    def __repr__(self) -> str:
        return f'{"|" if self.marked else ""}{self.n}{"|" if self.marked else ""}'


@dataclass
class Board:
    rows: list[list[BoardNumber]]

    def mark_number(self, number: int):
        for row in self.rows:
            for col in row:
                if col.n == number:
                    col.marked = True

    def columns(self) -> list[list[BoardNumber]]:
        out = []
        cur_col = []
        for i in range(len(self.rows[0])):
            for row in self.rows:
                cur_col.append(row[i])

            out.append(cur_col)
            cur_col = []
        return out

    def wins(self) -> tuple[bool, str]:
        for (i, row) in enumerate(self.rows):
            if all(n.marked for n in row):
                return True, f'won at row {i}, {row}'

        # for every column, if the column is all marked
        return any(all(self.rows[r][c].marked for r in range(len(self.rows))) for c in range(len(self.rows[0]))), ''

    def numbers(self) -> list[BoardNumber]:
        return list(itertools.chain(*self.rows))

    def __repr__(self) -> str:
        out = []
        for line in self.rows:
            out.append(" ".join(f'{repr(l):<4}' for l in line))

        return "\n".join(out)

    @staticmethod
    def from_input(s: list[str]):
        rows = []
        for line in s:
            rows.append(list(map(BoardNumber, map(int, map(str.strip, line.split())))))

        return Board(rows)


def part_1(input: str) -> str:
    random_numbers_str, split = input.split("\n", 1)

    random_numbers = map(int, random_numbers_str.split(","))

    boards: list[Board] = []
    for line in split[1:].split("\n\n"):
        s = line.splitlines()
        boards.append(Board.from_input(s))

    for i, number in enumerate(random_numbers):
        for board in boards:
            board.mark_number(number)

            if (wins := board.wins())[0]:
                summed = sum(n.n for n in board.numbers() if not n.marked)
                return f'{summed} * {number} = {summed * number}'

    return '???'


def part_2(input: str) -> str:
    random_numbers_str, split = input.split("\n", 1)

    random_numbers = map(int, random_numbers_str.split(","))

    boards: list[Board] = []
    for line in split[1:].split("\n\n"):
        s = line.splitlines()
        boards.append(Board.from_input(s))

    for i, number in enumerate(random_numbers):
        for (board_num, board) in enumerate(boards):
            board.mark_number(number)

            if (wins := board.wins())[0]:
                if len([b for b in boards if b.wins()[0]]) == len(boards):
                    nums = [n.n for n in board.numbers() if not n.marked]
                    summed = sum(nums)

                    return f'{summed} * {number} = {summed * number}'

    return f'???'
