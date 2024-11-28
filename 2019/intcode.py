class IntCodeComputer:
    N_PARAMS = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 99: 0}

    def __init__(self, program):
        self.program = program
        self._c = 0  # cursor

    def compute(self):
        while True:
            opcode, modes = self._parse(self.program[self._c])
            if opcode == 99:
                break
            elif opcode == 1:
                self.add(modes)
            elif opcode == 2:
                self.multiply(modes)
            elif opcode == 3:
                self.get_input(modes)
            elif opcode == 4:
                self.write_output(modes)
            elif opcode == 5:
                self.jump_if_true(modes)
            elif opcode == 6:
                self.jump_if_false(modes)
            elif opcode == 7:
                self.less_than(modes)
            elif opcode == 8:
                self.equals(modes)
            else:
                raise RuntimeError("Invalid instruction")

    def _parse(self, i):
        opcode = i % 100
        i //= 100

        modes = []
        for _ in range(self.N_PARAMS[opcode]):
            modes.append(i % 10)
            i //= 10

        return opcode, modes

    def get_value(self, n, pm):
        if pm == 0:
            # position mode
            return self.program[n]
        elif pm == 1:
            # immediate mode
            return n

    def add(self, modes):
        a, b, loc = self.program[self._c + 1 : self._c + 4]
        self.program[loc] = self.get_value(a, modes[0]) + self.get_value(b, modes[1])
        self._c += 4

    def multiply(self, modes):
        a, b, loc = self.program[self._c + 1 : self._c + 4]
        self.program[loc] = self.get_value(a, modes[0]) * self.get_value(b, modes[1])
        self._c += 4

    def get_input(self, modes):
        loc = self.program[self._c + 1]
        self.program[loc] = int(input("input please: "))
        self._c += 2

    def write_output(self, modes):
        print(self.get_value(self.program[self._c + 1], modes[0]))
        self._c += 2

    def jump_if_true(self, modes):
        p1, p2 = self.program[self._c + 1 : self._c + 3]
        if self.get_value(p1, modes[0]) != 0:
            self._c = self.get_value(p2, modes[1])
        else:
            self._c += 3

    def jump_if_false(self, modes):
        p1, p2 = self.program[self._c + 1 : self._c + 3]
        if self.get_value(p1, modes[0]) == 0:
            self._c = self.get_value(p2, modes[1])
        else:
            self._c += 3

    def less_than(self, modes):
        p1, p2, p3 = self.program[self._c + 1 : self._c + 4]
        if self.get_value(p1, modes[0]) < self.get_value(p2, modes[1]):
            self.program[p3] = 1
        else:
            self.program[p3] = 0
        self._c += 4

    def equals(self, modes):
        p1, p2, p3 = self.program[self._c + 1 : self._c + 4]
        if self.get_value(p1, modes[0]) == self.get_value(p2, modes[1]):
            self.program[p3] = 1
        else:
            self.program[p3] = 0
        self._c += 4
