import re
import sys
from collections import defaultdict


def answer(path):
    with open(path) as f:
        claims_raw = f.read().strip().split("\n")
    claims = []
    for c in claims_raw:
        m = re.search(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", c)
        claims.append(
            (
                int(m.group(2)),
                int(m.group(3)),
                int(m.group(4)),
                int(m.group(5)),
                m.group(1),
            )
        )

    claimed = defaultdict(lambda: 0)

    for claim in claims:
        for i in range(claim[2]):
            for j in range(claim[3]):
                claimed[(claim[0] + i, claim[1] + j)] += 1

    for claim in claims:
        n_claims = set(
            claimed[(claim[0] + i, claim[1] + j)]
            for i in range(claim[2])
            for j in range(claim[3])
        )
        if n_claims == {1}:
            return claim[4]


if __name__ == "__main__":
    print(answer(sys.argv[1]))
