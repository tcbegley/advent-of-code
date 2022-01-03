import re
import sys
from collections import Counter, defaultdict
from datetime import datetime

LOG_PATTERN = re.compile(r"\[([-: \d]+)\] (.+)")
NUMBER_PATTERN = re.compile(r"\d+")


def load_data(path):
    def process_pair(pair):
        timestamp, event = pair
        return (
            datetime.strptime(timestamp, "%Y-%m-%d %H:%M"),
            event,
        )

    with open(path) as f:
        return sorted(map(process_pair, LOG_PATTERN.findall(f.read())))


def get_time_asleep(logs):
    time_asleep = defaultdict(Counter)

    current_guard, start_minute = None, None
    for timestamp, event in logs:
        if event == "falls asleep":
            start_minute = timestamp.minute
        elif event == "wakes up":
            for minute in range(start_minute, timestamp.minute):
                time_asleep[current_guard][minute] += 1
        else:
            current_guard = NUMBER_PATTERN.search(event).group()

    return time_asleep


def part_1(logs):
    time_asleep = get_time_asleep(logs)

    most_asleep = max(
        time_asleep, key=lambda guard: time_asleep[guard].total()
    )
    time_most_asleep = max(
        time_asleep[most_asleep],
        key=lambda minute: time_asleep[most_asleep][minute],
    )
    return int(most_asleep) * time_most_asleep


def count_from_item(item):
    _, count = item
    return count


def count_from_guard_item_pair(pair):
    _, (_, count) = pair
    return count


def part_2(logs):
    time_asleep = get_time_asleep(logs)

    guard, (minute, _) = max(
        (
            (guard, max(counts.items(), key=count_from_item))
            for guard, counts in time_asleep.items()
        ),
        key=count_from_guard_item_pair,
    )

    return int(guard) * minute


if __name__ == "__main__":
    logs = load_data(sys.argv[1])
    print(f"Part 1: {part_1(logs)}")
    print(f"Part 2: {part_2(logs)}")
