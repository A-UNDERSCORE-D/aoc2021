from __future__ import annotations
from dataclasses import dataclass, field
from typing import DefaultDict, Dict


@dataclass
class Node:
    name: str
    small: bool = False
    max_visit = -1
    neighbours: list[Node] = field(default_factory=list)

    def __post_init__(self):
        self.small = self.name == self.name.lower()

        if self.small:
            if self.name in ('start', 'end'):
                self.max_visit = 1

            else:
                self.max_visit = 2

    def __repr__(self) -> str:
        return self.name

    def __lt__(self, other):
        return self.name < other.name


def create_graph(input: list[str]):
    nodes_s: list[tuple[str, str]] = []
    for line in input:
        start, end = line.split('-')
        nodes_s.append((start, end))

    nodes: dict[str, Node] = {}

    for (start, end) in nodes_s:
        start_node: Node | None = None
        end_node: Node | None = None
        if start in nodes:
            start_node = nodes[start]

        else:
            start_node = Node(start)
            nodes[start] = start_node

        if end in nodes:
            end_node = nodes[end]

        else:
            end_node = Node(end)
            nodes[end] = end_node

        if start not in end_node.neighbours:
            end_node.neighbours.append(start_node)

        if end not in start_node.neighbours:
            start_node.neighbours.append(end_node)

    return nodes


TEST_1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

TEST_2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

TEST_3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


def part_1(input: str) -> str:
    graph = create_graph(input.splitlines())
    paths = recursive_bfs(graph['end'], [], [], graph['start'], True)

    return f'{len(paths)}'


def recursive_bfs(end: Node, paths: list[Node], current_path: list[Node], current_node: Node, p1: bool) -> list[list[Node]]:
    out: list[list[Node]] = []
    current_path.append(current_node)
    for neighbour in current_node.neighbours:
        if neighbour == end:
            out.append(current_path.copy() + [end])
            continue

        if neighbour.name == 'start':
            continue

        if p1:
            if neighbour.small and neighbour in current_path:
                continue  # cant go over smalls twice

        else:
            """
            In part 2, you may visit any single small cave twice.

            To deal with that, if we have visited any small cave twice, we behave as normal
            """
            smalls: Dict[str, int] = DefaultDict(int)

            for n in current_path:
                if n.small:
                    smalls[n.name] += 1

            if neighbour.small and any(c >= 2 for c in smalls.values()) and neighbour in current_path:
                p1 = True
                continue

        res = recursive_bfs(end, paths, current_path.copy(), neighbour, p1=p1)
        out.extend(res)  # type: ignore
    return out


def part_2(input: str) -> str:
    graph = create_graph(input.splitlines())
    paths = recursive_bfs(graph['end'], [], [], graph['start'], p1=False)

    return f'{len(paths)}'
