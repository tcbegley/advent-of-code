class IntCodeComputer:
    def __init__(self, program):
        self.program = program
        self.cursor = 0

    def compute(self):
        while True:
            instruction = self.program[self.cursor]
            if instruction == 99:
                break
            elif instruction == 1:
                self.add()
            elif instruction == 2:
                self.multiply()
            else:
                raise RuntimeError("Invalid instruction")

    def add(self):
        a, b, loc = self.program[self.cursor + 1: self.cursor + 4]
        self.program[loc] = self.program[a] + self.program[b]
        self.cursor += 4

    def multiply(self):
        a, b, loc = self.program[self.cursor + 1: self.cursor + 4]
        self.program[loc] = self.program[a] * self.program[b]
        self.cursor += 4
