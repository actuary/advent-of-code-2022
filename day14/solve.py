from dataclasses import dataclass
from typing import Optional, Tuple


def get_data(filepath="input"):
    return open(filepath, "r").read().splitlines()


def test_data():
    return """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""".splitlines()


def fillin_cave(cave, path):
    vertices = zip(path[:-1], path[1:])

    for start, end in vertices:
        if start[0] == end[0]:
            if start[1] < end[1]:
                it = range(start[1], end[1] + 1)
            else:
                it = range(start[1], end[1] - 1, -1)

            for y in it:
                cave[y][start[0]] = "#"
        else:
            if start[0] < end[0]:
                it = range(start[0], end[0] + 1)
            else:
                it = range(start[0], end[0] - 1, -1)

            for x in it:
                cave[start[1]][x] = "#"


def normalise_path(path, min_x):
    return [(x - min_x, y) for x, y in path]


def create_cave(data):
    paths = [[tuple(int(el) for el in coord.split(",")) for coord in line.split(" -> ")] 
                   for line in data]

    min_y = 0
    max_y = max(max(y for _, y in path) for path in paths)
    min_x = 500 - max_y - 2
    max_x = 500 + max_y + 2

    cave = [["."]*(max_x - min_x + 1) for _ in range(min_y, max_y + 1)]

    paths = [normalise_path(path, min_x) for path in paths]

    for path in paths:
        fillin_cave(cave, path)

    sand_coord = (500 - min_x, 0)
    cave[sand_coord[1]][sand_coord[0]] = "+"

    return cave, sand_coord


def in_bounds(cave, pos):
    return 0 <= pos[1] < len(cave) and 0 <= pos[0] < len(cave[0])


def drop_sand(cave, sand_coord):
    directions_to_try = [(0, 1), (-1, 1), (1, 1)] 
    prev_pos = None
    pos = sand_coord
    while pos != prev_pos:
        for direction in directions_to_try:
            new_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if not in_bounds(cave, new_pos):
                prev_pos = pos
                if prev_pos != sand_coord:
                    cave[prev_pos[1]][prev_pos[0]] = "."
                return True
            elif cave[new_pos[1]][new_pos[0]] == ".":
                cave[new_pos[1]][new_pos[0]] = "*"
                prev_pos, pos = pos, new_pos
                if prev_pos != sand_coord:
                    cave[prev_pos[1]][prev_pos[0]] = "."
                break
            else:
                prev_pos = pos
    
    return pos == sand_coord


def part1(data=test_data()):
    cave, sand_coord = create_cave(data)

    i = 1
    while not drop_sand(cave, sand_coord):
        i+= 1

    return i


def part2(data=test_data()):
    cave, sand_coord = create_cave(data)
    cave.append(["."]*len(cave[0]))
    cave.append(["#"]*len(cave[0]))
     

    i = 1
    while not drop_sand(cave, sand_coord):
        i+= 1

    return i


if __name__ == "__main__":
    print(part1())
    print(part1(get_data()))
    print(part2())
    print(part2(get_data()))
