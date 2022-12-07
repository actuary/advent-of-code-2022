from dataclasses import dataclass
from typing import Optional, Tuple, List

def get_data(filepath="input"):
    return open(filepath, "r").read().splitlines()


def test_data():
    return """mjqjpqmgbljsphdztnvjfqwrcgsmlb
bvwbjplbgvbhsrlpgdmjqwftvncz
nppdvjthqldpwncqszvftbrmjlhg
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw""".splitlines()

def find_start_packet(data, pkt_size: int) -> List[int]:
    solutions = []
    for row in data:
        i = 0
        while len(set(row[i: i + pkt_size])) < pkt_size:
            i += 1
        solutions.append(i + pkt_size)

    return solutions

def part1(data=test_data()):
    return find_start_packet(data, 4)


def part2(data=test_data()):
    return find_start_packet(data, 14)

if __name__ == "__main__":
    print(part1())
    print(part1(get_data()))
    print(part2())
    print(part2(get_data()))
