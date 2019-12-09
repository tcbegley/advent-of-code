def answer(file_path):
    with open(file_path, "r") as f:
        steps = list(map(int, [x.strip() for x in f.readlines()]))
    i = 0
    count = 0
    n = len(steps)
    while True:
        tmp = i
        i += steps[i]
        if steps[tmp] >= 3:
            steps[tmp] -= 1
        else:
            steps[tmp] += 1
        count += 1
        if not 0 <= i < n:
            break
    return count


if __name__ == "__main__":
    print(answer("input/5.txt"))
