from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING


@dataclass
class Packet:
    version: int
    id: int

    def value(self) -> int:
        raise NotImplementedError


@dataclass
class LiteralPacket(Packet):
    data: int

    def __repr__(self) -> str:
        return f'LIT({self.data})'

    def value(self) -> int:
        return self.data


OPERATORS = {0: '+', 1: '*', 2: 'min', 3: 'max', 5: '>', 6: '<', 7: '=='}


@dataclass
class OperatorPacket(Packet):
    sub_packets: list[Packet] = field(default_factory=list)

    def __repr__(self) -> str:
        return f'OP {OPERATORS[self.id]} on {self.sub_packets}'

    def value(self) -> int:
        match self.id:
            case 0:
                return sum(p.value() for p in self.sub_packets)

            case 1:
                prod = self.sub_packets[0].value()

                for p in self.sub_packets[1:]:
                    prod *= p.value()

                return prod

            case 2:
                return min(p.value() for p in self.sub_packets)

            case 3:
                return max(p.value() for p in self.sub_packets)

            case 5:
                return 1 if self.sub_packets[0].value() > self.sub_packets[1].value() else 0

            case 6:
                return 1 if self.sub_packets[0].value() < self.sub_packets[1].value() else 0

            case 7:
                return 1 if self.sub_packets[0].value() == self.sub_packets[1].value() else 0

        raise ValueError(f'Unknown id {self.id}, {type(self.id)=}')


TYPE_LITERAL = 4


def string_pop(s: str, count: int) -> tuple[str, str]:
    return s[:count], s[count:]


def chomp_extra_data(s: str, current_len: int) -> str:
    while current_len % 4 != 0:
        s = s[1:]
        current_len += 1

    return s


def decode_packet(p: str, packet_total_length=0) -> tuple[Packet | None, str]:
    if TYPE_CHECKING:
        version: str | int
        pkt_id: str | int

    if not p:
        return None, ''

    version, p = string_pop(p, 3)
    pkt_id, p = string_pop(p, 3)

    version, pkt_id = int(version, 2), int(pkt_id, 2)
    packet_total_length += 6  # 3 bits for each header

    if pkt_id == 4:
        number: str = ""
        while True:
            n, p = string_pop(p, 5)
            number += n[1:]
            packet_total_length += 5
            if n[0] == '0':
                break

        chomp_extra_data(p, packet_total_length)

        return LiteralPacket(version, pkt_id, int(number, 2)), p

    # operator packet
    length_bit, p = string_pop(p, 1)
    packet_total_length += 1

    if length_bit == '0':
        sub_packet_data_len, p = string_pop(p, 15)
        packet_total_length += 15
        sub_packet_data, p = string_pop(p, int(sub_packet_data_len, 2))
        sub_packets = []
        while True:
            pkt, sub_packet_data = decode_packet(sub_packet_data, packet_total_length=packet_total_length)
            if pkt is None:
                break

            sub_packets.append(pkt)
            if sub_packet_data == '':
                break

        chomp_extra_data(p, packet_total_length)
        return OperatorPacket(version, pkt_id, sub_packets), p

    else:
        sub_packet_count, p = string_pop(p, 11)
        packet_total_length += 11
        sub_packets = []
        for _ in range(int(sub_packet_count, 2)):
            pkt, p = decode_packet(p, packet_total_length=packet_total_length)
            assert pkt is not None
            sub_packets.append(pkt)

        return OperatorPacket(version, pkt_id, sub_packets), p

    return None, p


# because python isnt being helpful

HEX = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}


def hex_str(s: str) -> str:
    return ''.join(HEX[c] for c in s)


def decode_packets(p: str) -> list[Packet]:
    out = []
    raw = ''
    for c in p:
        raw += HEX[c]

    while True:
        pk, p = decode_packet(raw)
        if pk is None or p == '':
            break

        out.append(pk)

    return out


def sum_versions(p: Packet) -> int:
    if isinstance(p, OperatorPacket):
        return p.version + sum(sum_versions(sp) for sp in p.sub_packets)

    return p.version


def part_1(input: str) -> str:
    p, leftover = decode_packet(hex_str(input))
    assert p is not None
    return f'{sum_versions(p)}'


def part_2(input: str) -> str:
    p, leftover = decode_packet(hex_str(input))
    assert p is not None
    return str(p.value())
