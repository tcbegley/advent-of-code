import sys


def load_data(path):
    def process_policy(policy):
        policy = policy.strip().split()
        lower, upper = [int(i) for i in policy[0].split("-")]
        letter = policy[1].rstrip(":")
        return lower, upper, letter, policy[2]

    with open(path) as f:
        return [process_policy(p) for p in f.readlines()]


def valid_1(lower, upper, letter, password):
    return lower <= password.count(letter) <= upper


def valid_2(lower, upper, letter, password):
    chars = set((password[lower - 1], password[upper - 1]))
    return len(chars) == 2 and letter in chars


def count_valid(valid, policies):
    return sum(valid(*p) for p in policies)


if __name__ == "__main__":
    policies = load_data(sys.argv[1])
    print(f"Part 1: {count_valid(valid_1, policies)}")
    print(f"Part 2: {count_valid(valid_2, policies)}")
