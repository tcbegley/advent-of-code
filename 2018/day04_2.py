import re
import sys
from collections import defaultdict
from datetime import datetime


def answer(path):
    with open(path) as f:
        logs_raw = f.read().strip().split("\n")

    log_pattern = re.compile(r"\[(.*)\] (.*)")
    logs = []

    for log in logs_raw:
        m = log_pattern.match(log)
        logs.append((m.group(1), m.group(2)))

    logs = sorted(logs, key=lambda x: x[0])

    asleep_time = defaultdict(lambda: {i: 0 for i in range(60)})

    current_guard = None
    start_minute, end_minute = None, None

    for log in logs:
        if log[1] == "falls asleep":
            start_minute = int(log[0][-2:])
        elif log[1] == "wakes up":
            end_minute = int(log[0][-2:])
            for i in range(start_minute, end_minute):
                asleep_time[current_guard][i] += 1
        else:
            current_guard = int(re.search(r"#(\d+)", log[1]).group(1))

    max_count = 0
    most_asleep = None

    for guard, times in asleep_time.items():
        time = sorted(
            [(k, v) for k, v in times.items()],
            key=lambda x: x[1],
            reverse=True,
        )[0]

        if time[1] > max_count:
            max_count = time[1]
            most_asleep = guard

    time = sorted(
        [(k, v) for k, v in asleep_time[most_asleep].items()],
        key=lambda x: x[1],
        reverse=True,
    )[0][0]

    return most_asleep * time


if __name__ == "__main__":
    print(answer(sys.argv[1]))
