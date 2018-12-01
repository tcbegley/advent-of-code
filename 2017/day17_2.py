def answer():
    pos = 0
    skip = 366
    after_zero = None
    for i in range(1, 50000001):
        pos = (pos + skip) % i + 1
        if pos == 1:
            after_zero = i
    return after_zero


if __name__ == "__main__":
    print(answer())
