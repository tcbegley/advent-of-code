b = 57
c = b
b *= 100
b += 100000
c = b
c += 17000
h = 0
for b in range(105700, 122701, 17):
    f = 1
    d = 2
    for d in range(2, b):
        if b % d == 0:
            f = 0
            break
    if f == 0:
        h += 1
print(h)
