import sys
from functools import reduce


def load_data(path):
    with open(path) as f:
        rules, my_ticket, nearby_tickets = f.read().strip().split("\n\n")

    rules = [process_rule(rule) for rule in rules.split("\n")]

    my_ticket = [int(i) for i in my_ticket.split("\n", 1)[1].split(",")]
    nearby_tickets = [
        [int(i) for i in t.split(",")] for t in nearby_tickets.split("\n")[1:]
    ]

    return rules, my_ticket, nearby_tickets


def process_rule(rule):
    field, constraints = rule.split(": ")
    constraints = [
        [int(i) for i in c.split("-")] for c in constraints.split(" or ")
    ]
    return field, constraints


def part_1(rules, tickets):
    invalid = 0
    for t in tickets:
        for n in t:
            if all(
                not ((c1[0] <= n <= c1[1]) or (c2[0] <= n <= c2[1]))
                for _, (c1, c2) in rules
            ):
                invalid += n

    return invalid


def part_2(rules, tickets, my_ticket):
    # filter valid tickets
    tickets = [
        ticket
        for ticket in tickets
        if all(
            any(
                (c1[0] <= n <= c1[1]) or (c2[0] <= n <= c2[1])
                for _, (c1, c2) in rules
            )
            for n in ticket
        )
    ]

    n_fields = len(rules)
    possible = [set(range(n_fields)) for _ in range(n_fields)]

    # for each rule, remove any column that has a violation
    for i, (_, (c1, c2)) in enumerate(rules):
        for j in range(n_fields):
            if not all(
                (c1[0] <= t[j] <= c1[1]) or (c2[0] <= t[j] <= c2[1])
                for t in tickets
            ):
                possible[i].remove(j)

    # not all columns will be uniquely determined automatically, but we can
    # remove fields that are the only possibility elsewhere
    while any(len(p) > 1 for p in possible):
        locked = [next(iter(p)) for p in possible if len(p) == 1]
        for p in possible:
            if len(p) == 1:
                continue
            else:
                for i in locked:
                    if i in p:
                        p.remove(i)

    # convert singleton sets to integers
    possible = [next(iter(p)) for p in possible]

    # departure fields are the first 6
    return reduce(lambda a, b: a * b, [my_ticket[i] for i in possible[:6]])


if __name__ == "__main__":
    rules, my_ticket, nearby_tickets = load_data(sys.argv[1])
    print(f"Part 1: {part_1(rules, nearby_tickets)}")
    print(f"Part 2: {part_2(rules, nearby_tickets, my_ticket)}")
