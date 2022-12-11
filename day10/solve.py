from dataclasses import dataclass
from typing import Optional, Tuple
import itertools

def get_data(filepath="input"):
    return open(filepath, "r").read().splitlines()


def test_data():
    return """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""".splitlines()

def test_small_data():
    return """noop
addx 3
addx -5""".splitlines()

def part1(data=test_data()):
    results = {}
    X = 1
    cycle = 0
    for line in data:
        match line.split():
            case ["addx", V]:
                cycle += 2
                results[cycle-1] = X
                X += int(V)
                results[cycle] = X
            case ["noop"]:
                cycle += 1
                results[cycle] = X

    return sum(results[i] * i for i in range(20, cycle+1, 40))


def crt_to_str(crt) -> str:
    return "\n".join(["".join(row) for row in crt])


def part2(data=test_data()):
    results = {}
    cycle = 0
    X = 1
    crt = [["."]*40 for _ in range(6)]
    for line in data:
        match line.split():
            case ["addx", V]:
                cycle += 2
                results[cycle-1] = X
                X += int(V)
                results[cycle] = X
            case ["noop"]:
                cycle += 1
                results[cycle] = X

    for cycle, sprite_pos in results.items():
        if sprite_pos - 1 <= cycle % 40 <= sprite_pos + 1:
            crt[cycle//40][cycle%40] = "#"
    
    print()
    print(crt_to_str(crt))


if __name__ == "__main__":
    print(part1())
    print(part1(get_data()))
    print(part2())
    print(part2(get_data()))
