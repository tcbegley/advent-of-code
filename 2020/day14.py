import sys


class Computer:
    def __init__(self):
        self.mem = {}
        self.mask = None

    def decode1(self, instructions):
        def decoder(addr, val, mem):
            masked_val = "".join(
                m if m != "X" else v
                for m, v in zip(self.mask, self.to_bin(val))
            )
            mem[addr] = int(masked_val, 2)

        return self._decode(instructions, decoder)

    def decode2(self, instructions):
        def decoder(addr, val, mem):
            masked_addr = "".join(
                m if m != "0" else v
                for m, v in zip(self.mask, self.to_bin(addr))
            )
            for a in self.generate_addresses(masked_addr):
                mem[int(a, 2)] = val

        return self._decode(instructions, decoder)

    def _decode(self, instructions, decoder):
        for ins in instructions:
            if ins[0] == "mask":
                self.mask = ins[1]
            else:
                addr = int(ins[0].lstrip("mem[").rstrip("]"))
                decoder(addr, int(ins[1]), self.mem)

        return sum(self.mem.values())

    @staticmethod
    def generate_addresses(mask):
        def generate_addresses_rec(mask, start):
            if not any(c == "X" for c in mask):
                yield mask
            else:
                for i, c in enumerate(mask):
                    if i < start:
                        continue
                    if c == "X":
                        yield from generate_addresses_rec(
                            mask[:i] + "0" + mask[i + 1 :], i
                        )
                        yield from generate_addresses_rec(
                            mask[:i] + "1" + mask[i + 1 :], i
                        )

        return generate_addresses_rec(mask, 0)

    @staticmethod
    def to_bin(n):
        s = ""
        while n:
            s = str(n % 2) + s
            n //= 2
        return s.zfill(36)


def load_data(path):
    with open(path) as f:
        return [line.split(" = ") for line in f.read().strip().split("\n")]


def part_1(instructions):
    c = Computer()
    return c.decode1(instructions)


def part_2(instructions):
    c = Computer()
    return c.decode2(instructions)


if __name__ == "__main__":
    instructions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(instructions)}")
    print(f"Part 2: {part_2(instructions)}")
