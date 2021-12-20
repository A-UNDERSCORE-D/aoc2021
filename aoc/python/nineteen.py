from __future__ import annotations

this doesnt work
from dataclasses import dataclass, field
import math
import itertools
from typing import TYPE_CHECKING, cast
try:
    from functools import cache
except ImportError:
    from functools import lru_cache as cache


@dataclass
class Scanner:
    id: int
    facing: tuple[str, str, str] | None = None
    beacons: set[Beacon] = field(default_factory=set)

    @cache
    def beacon_distances(self) -> list[float]:
        return [x.distance_to(y) for x in self.beacons for y in self.beacons if x != y]

    def __hash__(self) -> int:
        return self.id


@dataclass
class Beacon:
    x: int
    y: int
    z: int
    three_dimensions: bool = False
    neighbours: set[Beacon] = field(default_factory=set)

    true_position: tuple[int, int, int] | None = None

    @cache
    def distance_to(self, other: Beacon):
        if self.three_dimensions:
            return math.sqrt(
                ((other.x - self.x)**2) +
                ((other.y - self.y)**2) +
                ((other.z - self.z)**2)
            )

        return math.sqrt(((other.x - self.x)**2) + ((other.y - self.y)**2))

    def reorder_coords(self, new_order: tuple[str, str, str]) -> tuple[int, int, int]:
        dc = {'x': self.x, 'y': self.y, 'z': self.z}

        out = []

        for o in new_order:
            neg = o[0] == '-'
            if neg:
                o = o[1:]

                out.append(-dc[o])

            else:
                out.append(dc[o])

        return (out[0], out[1], out[2])

    @property
    def coords(self) -> tuple[int, int, int]:
        return (self.x, self.y, self.z)

    def could_eq(self, other: Beacon) -> tuple[bool, tuple[str, str, str] | None]:
        c = self.coords
        for permut in possible_directions:
            if c == other.reorder_coords(permut):
                return True, permut

        return False, None

    @staticmethod
    def from_line(line: str) -> Beacon:
        split = line.split(',')
        if len(split) == 3:
            return Beacon(int(split[0]), int(split[1]), int(split[2]), three_dimensions=True)

        else:
            return Beacon(int(split[0]), int(split[1]), -1)

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Beacon):
            raise ValueError(f'cant eq with {type(__o)} {__o}')

        o = __o
        return self.x == o.x and self.y == o.y and self.z == o.z

    def with_offset(self, x: int, y: int, z: int) -> Beacon:
        return Beacon(self.x+x, self.y+y, self.z+z)


def parse_input(input: str) -> list[Scanner]:
    out = []
    scanner_lines = input.split('\n\n')
    for s in scanner_lines:
        lines = s.splitlines()
        header, lines = lines[0], lines[1:]
        S = Scanner(int(header.split()[2]))
        out.append(S)

        for b_l in lines:
            S.beacons.add(Beacon.from_line(b_l))

        # for b in S.beacons:
            # b.neighbours.update({x for x in S.beacons if x != b})

    return out


EPSILON = 0.1

# it must contain one of x, y, and z, negative or not
POS = ('x', 'y', 'z')
NEG = tuple(('-' + thing for thing in POS))
ALL = POS + NEG


def _okay(permut: tuple[str, str, str]):
    if not all((p in permut or n in permut) for p, n in zip(POS, NEG)):
        return False

    if any(p in permut and n in permut for p, n in zip(POS, NEG)):
        return False

    return True


possible_directions: list[tuple[str, str, str]] = list(filter(_okay, itertools.permutations(ALL, 3)))  # type: ignore

POSSIBLE_CHANGES = ('x', 'y', 'z', '-x', '-y', '-z')


def brute(previous_offsets: list[int], current_order: list[str | None], target_coord: int, skip_permuts: list[str], true_beacons: list[Beacon], false_beacons: list[Beacon], start_offset: int = -2000):
    options = [p for p in POSSIBLE_CHANGES if not any(x in current_order for x in (p, '-'+p if len(p) == 1 else p[1:]))]
    for offset in range(start_offset, 2000):
        count = 0
        for b in true_beacons:
            b_c = b.coords
            b_t = b_c[target_coord]
            for other in false_beacons:
                for n_t in options:
                    if n_t in skip_permuts:
                        continue

                    start = [s if s is not None else 'x' for s in current_order]
                    start[target_coord] = n_t
                    other_reordered = other.reorder_coords((start[0], start[1], start[2]))

                    properly_offset: list[int | None] = [None, None, None]
                    for i, po in enumerate(previous_offsets):
                        properly_offset[i] = other_reordered[i]+po

                    properly_offset[target_coord] = other_reordered[target_coord]+offset

                    CONT = False
                    for (bc, oc) in zip(b_c, properly_offset):
                        # if offset == -1246 and other.coords[0] == 686:
                        #     print(bc, oc)
                        if oc is None:
                            continue

                        if bc != oc:
                            CONT = True
                            break

                    if CONT:
                        continue

                    # if not all(bc == oc for bc, oc in zip(b_c, properly_offset)):
                    #     continue

                    count += 1
                    # if count > 6:
                    #     print(count)
                    if count >= 12:
                        # print('returning!', offset, n_t, count)
                        return offset, n_t


def solve(scanners: list[Scanner]):
    """
    place scanner 0 at 0,0

    create graph of its points in absolute space

    for each scanner, bfs out from 0,0 and find where the coordinates align if correctly offset


    """
    # true_area is the full world, with 0,0 being scanner 1
    true_area: dict[tuple[int, int, int], Beacon | Scanner] = {}
    whatever = ('x', 'y', 'z', '-x', '-y', '-z')
    # scanners = scanners[1:]
    zero = scanners[0]
    scanners = scanners[1:]
    for b in zero.beacons:
        true_area[b.coords] = b

    true_area[(0, 0, 0)] = zero

    scanners_to_find = scanners.copy()
    # scanners_to_find.pop(0)

    while scanners_to_find:
        print()
        s = scanners_to_find[0]

        found_scanners = [(pos, s) for pos, s in true_area.items() if isinstance(s, Scanner)]
        print(f'We have found {len(found_scanners)} (out of {len(scanners)})')

        order: list[str] = [None, None, None]  # type: ignore
        offset: list[int] = [None, None, None]  # type: ignore
        sat_loc_used = None

        # find the location of the scanner
        for (loc, found_s) in found_scanners:
            print(f'Trying to find location for {s.id} with found sat {found_s.id} at {loc}')
            n_order: list[str | None] = [None, None, None]
            n_offset: list[int | None] = [None, None, None]
            skips: list[list[str]] = [[], [], []]
            bacons = [b.with_offset(*loc) for b in found_s.beacons]
            sat_loc_used = loc

            total = 0
            while total < 3:
                # start_offset: int = -2000
                # if n_offset[total] is not None and n_offset[total] <= 2000:  # type: ignore
                #     start_offset = n_offset[total]  # type: ignore
                #     print(f'\tUsing start offset {start_offset} (skipping )')

                res = brute(
                    [o for o in n_offset[:total] if o is not None],
                    n_order,
                    total,
                    skips[total],
                    list(found_s.beacons),
                    list(s.beacons),
                    # start_offset
                )
                if res is None:
                    if total == 0:
                        print(f'\tcannot find position for {s.id} and {found_s.id}, skipping')
                        break

                    total -= 1
                    # we can backtrack
                    skips[total].append(n_order[total])  # type: ignore
                    print(f'\tbacktracking... adding {n_order[total]} to skips: {skips}')
                    n_order[total] = None
                    # n_offset[total] = None
                    print('\t', n_order, n_offset)

                else:
                    n_offset[total], n_order[total] = res
                    print(f'\tFound {("x", "y", "z")[total]}: {n_offset[total]}')
                    total += 1

            # for i in range(3):
            #     res = brute([o for o in n_offset if o is not None], n_order, i, bacons, list(s.beacons))
            #     if res is None:
            #         print(f'\tcannot find position for {s.id} and {found_s.id}, skipping')
            #         break

            #     n_offset[i], n_order[i] = res
            #     print(f'\tFound {("x", "y", "z")[i]}: {n_offset[i]}')

            if None not in n_order and None not in n_offset:
                offset = n_offset  # type: ignore
                order = n_order  # type: ignore
                break

        if None in offset:
            print(f'\tfailed to find position for {s.id}')
            scanners_to_find.append(scanners_to_find.pop(0))
            continue

        scanners_to_find.pop(0)
        offset_s = cast('list[int]', offset)
        true_s_position = (-(offset_s[0] + -sat_loc_used[0]), -(offset_s[1] +
                           -sat_loc_used[1]), -(offset_s[2] + -sat_loc_used[2]))

        true_area[true_s_position] = s
        print(f'scanner id {s.id} is at {true_s_position}, with facing {order}')

        for beacon in s.beacons:
            true_position: tuple[int, int, int] = tuple(  # type:ignore
                [p+o for p, o in zip(beacon.reorder_coords((order[0], order[1], order[2])), true_s_position)]
            )
            beacon.true_position = true_position

            if true_position not in true_area:
                true_area[true_position] = beacon

        s.facing = (order[0], order[1], order[2])


def part_1(input: str) -> str:
    input = TEST
    scanners = parse_input(input)

    solve(scanners)
    return ''


def part_2(input: str) -> str:
    return ''


TEST = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""
