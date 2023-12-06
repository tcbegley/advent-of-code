import sys
from dataclasses import dataclass


# each map can be considered as a partition of the integers with corresponding offsets
# given an interval like Interval(0, 10, 2), this would first map [0, 10) to [2, 12),
# then we apply subsequent maps. Therefore to compose the maps, we start at the end,
# then iteratively offset intervals, overlay them on the ones we already have, and
# split accordingly. So in the above example, if the existing map were
# [Interval(-inf, 5, 0), Interval(5, 14, 3), Interval(15, inf, 0)]
# then after composing with Interval(0, 10, 2) we would have
# [Interval(-inf, 0, 0), Interval(0, 3, 2), Interval(3, 10, 5), Interval(10, 15, 3),
# Interval(15, inf, 0)].
# note here we split on 3 because 3 is offset first by 2 to 5, then falls into the range
# of the later map
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
    # sorting intervals makes padding gaps etc. much easier
    return sorted(intervals, key=lambda m: m.low)


def load_data(path) -> tuple[list[int], list[Map]]:
    with open(path) as f:
        seeds, *blocks = f.read().strip().split("\n\n")
    seeds = list(map(int, seeds.removeprefix("seeds:").strip().split(" ")))
    maps = [parse_block(block) for block in blocks]
    # reverse the order of the maps so we can compose them (final is applied first)
    return seeds, maps[::-1]


def intersect(a: Interval, b: Interval) -> bool:
    # return True if intervals a and b intersect
    return (a.low <= b.low < a.high) or (b.low <= a.low < b.high)


def map_interval(interval: Interval, map_: Map) -> Map:
    # given a single interval and a map, return a list of intervals corresponding to a
    # map of the values in interval
    offset_interval = Interval(
        interval.low + interval.offset, interval.high + interval.offset, 0
    )
    mapped_interval = (
        Interval(
            max(offset_interval.low, other.low),
            min(offset_interval.high, other.high),
            other.offset,
        )
        for other in map_
        if intersect(offset_interval, other)
    )
    return [
        Interval(
            i.low - interval.offset,
            i.high - interval.offset,
            i.offset + interval.offset,
        )
        for i in mapped_interval
        if interval.low < interval.high
    ]


def compose(left: Map, right: Map) -> Map:
    composed = []
    for interval in left:
        composed.extend(map_interval(interval, right))
    return composed


def pad_intervals(intervals):
    # adds intervals with 0 offset to a list of intervals to convert it to a partition
    # of the integers. useful when composing maps to ensure we don't miss anything
    if not intervals:
        return [Interval(float("-inf"), float("inf"), 0)]
    padded_intervals = [Interval(float("-inf"), intervals[0].low, 0)]

    for i, interval in enumerate(intervals):
        padded_intervals.append(interval)
        if i < len(intervals) - 1:
            padded_intervals.append(
                Interval(interval.high, intervals[i + 1].low, 0)
            )
        else:
            padded_intervals.append(Interval(interval.high, float("inf"), 0))

    return padded_intervals


def map_seed(seed: int, map_: Map) -> int:
    # given a seed and a map, find the interval containing seed and add the offset
    left, right = 0, len(map_)
    while left < right:
        mid = (left + right) // 2
        interval = map_[mid]
        if interval.low <= seed < interval.high:
            return seed + interval.offset
        elif seed < interval.low:
            right = mid
        else:
            left = mid + 1

    raise RuntimeError


def compose_maps(maps: list[Map]) -> Map:
    final_map = [Interval(float("-inf"), float("inf"), 0)]

    for map_ in maps:
        final_map = compose(pad_intervals(map_), final_map)

    return final_map


def part_1(seeds, final_map):
    return min(map_seed(seed, final_map) for seed in seeds)


def part_2(seeds, final_map):
    # this is a trick to iterate over the seeds in pairs
    iterator = [iter(seeds)] * 2
    seeds = [
        Interval(start, start + length, 0) for start, length in zip(*iterator)
    ]
    return min(i.low + i.offset for i in compose(seeds, final_map))


if __name__ == "__main__":
    seeds, maps = load_data(sys.argv[1])
    final_map = compose_maps(maps)
    print(f"Part 1: {part_1(seeds, final_map)}")
    print(f"Part 2: {part_2(seeds, final_map)}")
