import re
import sys
from collections import defaultdict


class TuringMachine:
    update = {
        'A': {0: [1, 1, 'B'], 1: [0, -1, 'C']},
        'B': {0: [1, -1, 'A'], 1: [1, 1, 'D']},
        'C': {0: [0, -1, 'B'], 1: [0, -1, 'E']},
        'D': {0: [1, 1, 'A'], 1: [0, 1, 'B']},
        'E': {0: [1, -1, 'F'], 1: [1, -1, 'C']},
        'F': {0: [1, 1, 'D'], 1: [1, 1, 'A']}
    }

    def __init__(self):
        self.state = 'A'
        self.check = 12481997
        self.tape = defaultdict(lambda: 0)
        self.pos = 0

    def move(self):
        todo = TuringMachine.update[self.state][self.tape[self.pos]]
        self.tape[self.pos] = todo[0]
        self.pos += todo[1]
        self.state = todo[2]

    def run(self):
        for _ in range(self.check):
            self.move()
        return sum(self.tape.values())


def answer():
    tm = TuringMachine()
    return tm.run()


if __name__ == "__main__":
    print(answer())
