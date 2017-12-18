def answer():
    l = [0]
    pos = 0
    skip = 366
    for i in range(1, 2018):
        pos = (pos + skip) % i + 1
        l.insert(pos, i)
    return l[l.index(2017) + 1]


if __name__ == "__main__":
    print(answer())
