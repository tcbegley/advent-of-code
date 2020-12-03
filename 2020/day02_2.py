import sys


def process_policy(policy):
    policy = policy.strip().split()
    lower, upper = [int(i) for i in policy[0].split("-")]
    letter = policy[1].rstrip(":")
    return lower, upper, letter, policy[2]


def valid(lower, upper, letter, password):
    chars = set((password[lower-1], password[upper-1]))
    return len(chars) == 2 and letter in chars


def answer(path):
    with open(path) as f:
        policies = map(process_policy, f.readlines())

    return sum(valid(*p) for p in policies)


if __name__ == "__main__":
    print(answer(sys.argv[1]))