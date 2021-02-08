import re
import sys

IP = re.compile(r"\[[a-z]*\]")
ABBA = re.compile(r"([a-z])([a-z])\2\1")
ABA = re.compile(r"([a-z])([a-z])\1")


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def supports_tls(ip):
    for hypernet_seq in IP.findall(ip):
        for match in ABBA.findall(hypernet_seq):
            if match[0] != match[1]:
                return False

    for supernet_seq in IP.split(ip):
        for match in ABBA.findall(supernet_seq):
            if match[0] != match[1]:
                return True

    return False


def find_aba(seq):
    for i in range(len(seq) - 2):
        chunk = seq[i : i + 3]
        if chunk[0] == chunk[2] and chunk[1] != chunk[0]:
            yield chunk


def supports_ssl(ip):
    abas = [
        aba for supernet_seq in IP.split(ip) for aba in find_aba(supernet_seq)
    ]
    abas = [aba for aba in abas if aba]
    return any(
        "{1}{0}{1}".format(*aba) in hypernet_seq
        for hypernet_seq in IP.findall(ip)
        for aba in abas
    )


def part_1(ips):
    return sum(map(supports_tls, ips))


def part_2(ips):
    return sum(map(supports_ssl, ips))


if __name__ == "__main__":
    ips = load_data(sys.argv[1])
    print(f"Part 1: {part_1(ips)}")
    print(f"Part 2: {part_2(ips)}")
