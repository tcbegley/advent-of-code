import sys
from dataclasses import dataclass
from tqdm.auto import tqdm
from collections import deque


@dataclass(frozen=True)
class Interval:
    low: int
    high: int
    offset: int


def parse_block(block):
    _, *block = block.split("\n")
    maps = []
    for row in block:
        dest, src, length = map(int, row.split(" "))
        maps.append(Interval(src, src + length, dest - src))
    return sorted(maps, key=lambda m: m.low)


def load_data(path):
    with open(path) as f:
        seeds, *blocks = f.read().strip().split("\n\n")
    seeds = list(map(int, seeds.removeprefix("seeds:").strip().split(" ")))
    maps = [parse_block(block) for block in blocks]
    return seeds, maps[::-1]


def map_intervals(intervals, maps):
    intervals = deque(intervals)
    maps = deque(maps)

    mapped_intervals = []
    while maps:
        map_ = maps.popleft()

        while True:
            interval = intervals.popleft()
            if interval.high <= map_.low:
                # intervals don't overlap
                mapped_intervals.append(interval)
            elif interval.high <= map_.high:
                # intervals overlap, but map_ extends beyond interval
                if interval.low < map_.low:
                    mapped_intervals.append(
                        Interval(interval.low, map_.low, interval.offset)
                    )
                    mapped_intervals.append(
                        Interval(
                            map_.low,
                            interval.high,
                            interval.offset + map_.offset,
                        )
                    )
                else:
                    mapped_intervals.append(
                        Interval(
                            interval.low,
                            interval.high,
                            interval.offset + map_.offset,
                        )
                    )
            else:
                # intervals overlap, interval extends beyond map
                if interval.low < map_.low:
                    mapped_intervals.append(
                        Interval(interval.low, map_.low, interval.offset)
                    )
                    mapped_intervals.append(
                        Interval(
                            map_.low,
                            map_.high,
                            interval.offset + map_.offset,
                        )
                    )
                else:
                    mapped_intervals.append(
                        Interval(
                            interval.low,
                            map_.high,
                            interval.offset + map_.offset,
                        )
                    )
                intervals.appendleft(
                    Interval(map_.high, interval.high, interval.offset)
                )
                break

    mapped_intervals.extend(intervals)

    return mapped_intervals


def map_seed(seed, intervals):
    for interval in intervals:
        if interval.low <= seed < interval.high:
            return seed + interval.offset

    raise RuntimeError


def part_1(seeds, maps):
    intervals = [Interval(float("-inf"), float("inf"), 0)]

    for m in maps:
        intervals = map_intervals(intervals, m)

    return [map_seed(seed, intervals) for seed in seeds]


def part_2(seeds, maps):
    new_seeds = []
    for start, length in zip(*([iter(seeds)] * 2)):
        new_seeds.extend(range(start, start + length))

    return part_1(new_seeds, maps)


if __name__ == "__main__":
    seeds, maps = load_data(sys.argv[1])
    print(f"Part 1: {part_1(seeds, maps)}")
    # print(f"Part 2: {part_2(seeds, maps)}")
