import sys
from dataclasses import dataclass, field
from functools import reduce
from typing import Optional


def load_data(path):
    with open(path) as f:
        hex_data = f.read().strip()

    data = bin(int(hex_data, base=16)).removeprefix("0b")

    # need to account for leading zeros
    num_bits = len(hex_data) * 4
    return data.zfill(num_bits)


@dataclass
class Packet:
    version: int
    type_id: int
    value: Optional[int] = None
    length_id: Optional[int] = None
    subpackets: list["Packet"] = field(default_factory=list)

    def __post_init__(self):
        if self.type_id == 0:
            self.value = sum(p.value for p in self.subpackets)
        elif self.type_id == 1:
            self.value = reduce(
                lambda x, y: x * y, (p.value for p in self.subpackets)
            )
        elif self.type_id == 2:
            self.value = min(p.value for p in self.subpackets)
        elif self.type_id == 3:
            self.value = max(p.value for p in self.subpackets)
        elif self.type_id == 5:
            self.value = int(
                self.subpackets[0].value > self.subpackets[1].value
            )
        elif self.type_id == 6:
            self.value = int(
                self.subpackets[0].value < self.subpackets[1].value
            )
        elif self.type_id == 7:
            self.value = int(
                self.subpackets[0].value == self.subpackets[1].value
            )


def parse_packets(data, limit=sys.maxsize):
    count = 0
    packets = []
    while data and count < limit:
        count += 1
        version, type_id, data = parse_header(data)
        if type_id == 4:
            value, data = parse_literal(data)
            packets.append(
                Packet(version=version, type_id=type_id, value=value)
            )
        elif data[0] == "0":
            num_bits, data = int(data[1:16], 2), data[16:]
            subpackets, data = data[:num_bits], data[num_bits:]
            packets.append(
                Packet(
                    version=version,
                    type_id=type_id,
                    length_id=0,
                    subpackets=parse_packets(subpackets)[0],
                )
            )
        else:
            num_subpackets, data = int(data[1:12], 2), data[12:]
            subpackets, data = parse_packets(data, limit=num_subpackets)
            packets.append(
                Packet(
                    version=version,
                    type_id=type_id,
                    length_id=1,
                    subpackets=subpackets,
                )
            )

    return packets, data


def parse_header(data):
    return int(data[:3], 2), int(data[3:6], 2), data[6:]


def parse_literal(data):
    blocks = []

    while data:
        last_block, block, data = data[0] == "0", data[1:5], data[5:]
        blocks.append(block)

        if last_block:
            break

    return int("".join(blocks), 2), data


def sum_versions(packets):
    return sum(
        packet.version + sum_versions(packet.subpackets) for packet in packets
    )


def part_1(data):
    packets, _ = parse_packets(data, limit=1)
    return sum_versions(packets)


def part_2(data):
    packets, _ = parse_packets(data, limit=1)
    return packets[0].value


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
