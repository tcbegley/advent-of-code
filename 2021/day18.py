import sys
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from itertools import permutations
from typing import Union


@dataclass
class Number:
    value: int = None
    parent: "Number" = None
    left: Union[int, "Number"] = None
    right: Union[int, "Number"] = None
    is_left_child: bool = None
    is_right_child: bool = None

    def __repr__(self):
        rep = "Number("
        first = True
        if self.value is not None:
            rep += f"{'' if first else ', '}value={self.value}"
            first = False
        if self.left:
            rep += f"{'' if first else ', '}left={self.left}"
            first = False
        if self.right:
            rep += f"{'' if first else ', '}right={self.right}"
            first = False
        rep += ")"
        return rep

    def to_list(self):
        if self.value is not None:
            return self.value
        return [self.left.to_list(), self.right.to_list()]

    def __add__(self, other):
        left = deepcopy(self)
        right = deepcopy(other)
        new = Number(left=left, right=right)
        left.parent = new
        left.is_left_child = True
        right.parent = new
        right.is_right_child = True
        return new

    def magnitude(self):
        if self.value is not None:
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()


def parse_number(number, parent=None, is_left_child=None, is_right_child=None):
    if isinstance(number, int):
        return Number(
            value=number,
            parent=parent,
            is_left_child=is_left_child,
            is_right_child=is_right_child,
        )
    current = Number(
        parent=parent,
        is_left_child=is_left_child,
        is_right_child=is_right_child,
    )
    left, right = number
    current.left = parse_number(
        left, parent=current, is_left_child=True, is_right_child=False
    )
    current.right = parse_number(
        right, parent=current, is_left_child=False, is_right_child=True
    )
    return current


def load_data(path):
    with open(path) as f:
        return [parse_number(eval(line.strip())) for line in f.readlines()]


def add_left(number, value):
    current = number
    ancestor = number.parent
    while ancestor is not None:
        if current.is_left_child:
            ancestor = ancestor.parent
            current = current.parent
        else:
            node = ancestor.left
            while node.right:
                node = node.right
            node.value += value
            break


def add_right(number, value):
    current = number
    ancestor = number.parent
    while ancestor is not None:
        if current.is_right_child:
            ancestor = ancestor.parent
            current = current.parent
        else:
            node = ancestor.right
            while node.left:
                node = node.left
            node.value += value
            break


def explode(number, depth=0):
    if number is None:
        return False
    elif (number.left is not None and number.left.value is not None) and (
        number.right is not None and number.right.value is not None
    ):
        # we've reached a terminal pair
        if depth >= 4:
            left, right = number.left.value, number.right.value
            add_left(number, left)
            add_right(number, right)
            number.value = 0
            number.left = number.right = None
            return True
        return False
    return explode(number.left, depth=depth + 1) or explode(
        number.right, depth=depth + 1
    )


def split(number):
    if number is None:
        return False
    elif number.value is not None and number.value >= 10:
        div, mod = divmod(number.value, 2)
        left, right = div, div + mod
        number.value = None
        number.left = Number(
            value=left, parent=number, is_left_child=True, is_right_child=False
        )
        number.right = Number(
            value=right,
            parent=number,
            is_left_child=False,
            is_right_child=True,
        )
        return True
    return split(number.left) or split(number.right)


def reduce_number(number):
    while True:
        if explode(number) or split(number):
            continue
        break
    return number


def part_1(data):
    return reduce(lambda x, y: reduce_number(x + y), data).magnitude()


def part_2(data):
    return max(reduce_number(x + y).magnitude() for x, y in permutations(data, 2))


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
