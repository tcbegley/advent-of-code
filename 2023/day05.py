import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Interval:
    low: int
    high: int
    offset: int


Map = list[Interval]


def parse_block(block: str) -> Map:
    _, *block = block.split("\n")
    intervals = []
    for row in block:
        dest, src, length = map(int, row.split(" "))
        intervals.append(Interval(src, src + length, dest - src))
    return sorted(intervals, key=lambda i: i.low)


def load_data(path) -> tuple[list[int], list[Map]]:
    with open(path) as f:
        seeds, *blocks = f.read().strip().split("\n\n")
    seeds = list(map(int, seeds.removeprefix("seeds:").strip().split(" ")))
    maps = [parse_block(block) for block in blocks]
    return seeds, maps


def intersect(a: Interval, b: Interval) -> bool:
    # return True if intervals a and b intersect
    return (a.low <= b.low < a.high) or (b.low <= a.low < b.high)


def map_intervals(intervals: list[Interval], map_: Map):
    mapped_intervals = []
    for interval in intervals:
        offset_interval = Interval(
            interval.low + interval.offset, interval.high + interval.offset, 0
        )
        for i in map_:
            if intersect(offset_interval, i):
                mapped_intervals.append(
                    Interval(
                        max(offset_interval.low, i.low) - interval.offset,
                        min(offset_interval.high, i.high) - interval.offset,
                        interval.offset + i.offset,
                    )
                )

    return mapped_intervals


def pad_intervals(intervals):
    # adds intervals with 0 offset to a list of intervals to convert it to a partition
    # of the integers. useful when composing maps to ensure we don't miss anything
    if not intervals:
        return [Interval(float("-inf"), float("inf"), 0)]
    padded_intervals = [Interval(float("-inf"), intervals[0].low, 0)]

    for i, interval in enumerate(sorted(intervals, key=lambda i: i.low)):
        padded_intervals.append(interval)
        if i < len(intervals) - 1:
            padded_intervals.append(Interval(interval.high, intervals[i + 1].low, 0))
        else:
            padded_intervals.append(Interval(interval.high, float("inf"), 0))

    return padded_intervals


def solve(intervals, maps):
    for map_ in maps:
        intervals = map_intervals(intervals, pad_intervals(map_))

    return min(i.low + i.offset for i in intervals)


def part_1(seeds, maps):
    return solve([Interval(seed, seed + 1, 0) for seed in seeds], maps)


def part_2(seeds, maps):
    # this is a trick to iterate over the seeds in pairs
    iterator = [iter(seeds)] * 2
    intervals = [Interval(start, start + length, 0) for start, length in zip(*iterator)]
    return solve(intervals, maps)


if __name__ == "__main__":
    seeds, maps = load_data(sys.argv[1])
    print(f"Part 1: {part_1(seeds, maps)}")
    print(f"Part 2: {part_2(seeds, maps)}")
