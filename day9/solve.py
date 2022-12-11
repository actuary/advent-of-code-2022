from dataclasses import dataclass
from typing import List, Set
from enum import Enum


def get_data(filepath="input"):
    return open(filepath, "r").read().splitlines()


def test_data():
    return """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".splitlines()

def test_part2():
    return """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""".splitlines()


@dataclass(frozen=True, eq=True)
class Position:
    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int) -> "Position":
        return Position(self.x * other, self.y * other)
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Direction(Enum):
    LEFT = Position(-1, 0)
    RIGHT = Position(1, 0)
    UP = Position(0, 1)
    DOWN = Position(0, -1)
    
    @staticmethod
    def from_str(val: str) -> "Direction":
        return STR_TO_DIRECTION[val]


STR_TO_DIRECTION = {
    "L": Direction.LEFT,
    "R": Direction.RIGHT,
    "U": Direction.UP,
    "D": Direction.DOWN
}


@dataclass
class Command:
    direction: Direction
    steps: int



@dataclass
class Rope:
    body: List[Position]

    @property
    def tail(self):
        return self.body[-1]

    @property
    def head(self) -> Position:
        return self.body[0]

    def __getitem__(self, idx: int) -> Position:
        return self.body[idx]

    def __setitem__(self, idx: int, data: Position) -> None:
        self.body[idx] = data

    def __len__(self) -> int:
        return len(self.body)

    def __str__(self) -> str:
        return " ".join(str(el) for el in self.body)


def move_piece(head: Position, tail: Position) -> Position:
    y_dist = abs(tail.y - head.y)
    x_dist = abs(tail.x - head.x)

    if y_dist == 2 and x_dist == 2:
        return Position(tail.x + 2 * (head.x - tail.x > 0) - 1, 
                        tail.y + 2 * (head.y - tail.y > 0) - 1)
    if y_dist == 2:
        return Position(head.x, 
                        tail.y + 2 * (head.y - tail.y > 0) - 1)
    elif x_dist == 2:
        return Position(tail.x + 2 * (head.x - tail.x > 0) - 1, 
                        head.y)
    return tail


def advance_rope(rope: Rope, direction: Direction) -> None:
    rope[0] = rope[0] + direction.value
    for i in range(1, len(rope)):
        rope[i] = move_piece(rope[i-1], rope[i])


def tail_visits(data, snake_size: int = 2) -> Set[Position]:
    rope = Rope([Position(0, 0) for _ in range(snake_size)])
    tail_visited = {rope.tail}
    for line in data:
        direction, steps = line.split(" ")
        command = Command(Direction.from_str(direction), int(steps))
        for _ in range(command.steps):
            advance_rope(rope, command.direction)
            tail_visited.add(rope.tail)

    return tail_visited


def part1(data=test_data()):
    visits = tail_visits(data, 2)
    return len(visits)


def part2(data=test_data()):
    visits = tail_visits(data, 10)
    # print_visited_graph(visited_graph(visits))
    return len(visits)


def print_visited_graph(visited):
    print("\n".join(["".join(row) for row in visited]))


def visited_graph(visited):
    width = max(-min(t.x for t in visited), max(t.x for t in visited)) * 2 + 1
    length = max(-min(t.y for t in visited), max(t.y for t in visited)) * 2 + 1
    x_offset = (width - 1)//2
    y_offset = (length - 1)//2

    pos_map = [["."]*width for _ in range(length)]
    for pos in visited:
        pos_map[length - (pos.y + y_offset) - 1][pos.x + x_offset] = "#"
    pos_map[length - y_offset - 1][x_offset] = "s"

    return pos_map


if __name__ == "__main__":
    print(part1())
    print(part1(get_data()))
    print(part2())
    print(part2(test_part2()))
    print(part2(get_data()))
