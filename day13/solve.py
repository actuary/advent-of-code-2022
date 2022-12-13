from dataclasses import dataclass
from typing import Optional, Tuple
from enum import Enum

def get_data(filepath="input"):
    return open(filepath, "r").read().splitlines()


def test_data():
    return """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""".splitlines()

# Element = [List|Number*]
#
#
#
#
#
#
test_data_2 = """[[4,4],4,4]
[[4,4],4,4,4]""".splitlines()

def parse_number(list_string: str, idx) -> Tuple[int, int]:
    value = 0
    while list_string[idx].isnumeric():
        value = value * 10 + int(list_string[idx])
        idx += 1

    return idx, value


def parse_list_element(list_string: str, idx) -> Tuple[int, list | int]:
    if list_string[idx] == "[":
        return parse_list(list_string, idx)
    elif list_string[idx].isnumeric():
        return parse_number(list_string, idx)

    raise RuntimeError


def parse_list(list_string: str, idx=0) -> Tuple[int, list | int]:
    if list_string[idx] == "[":
        value = []
        idx += 1
        while idx < len(list_string) and list_string[idx] != "]":
            idx += (list_string[idx] == ",")
            idx, element = parse_list_element(list_string, idx)
            value.append(element)
        return idx + 1, value
    elif list_string[idx].isnumeric():
        return parse_number(list_string, idx)

    raise RuntimeError

class Comparison(Enum):
    LESS = -1
    MORE = 0
    SAME = 1

def check_pair(pair: Tuple[list | int, list | int]) -> Comparison:
    match pair:
        case [*left], [*right]:
            for left_val, right_val in zip(left, right):
                result = check_pair((left_val, right_val))
                if result != Comparison.SAME:
                    return result
            
            if len(left) < len(right):
                return Comparison.LESS
            
            if len(left) == len(right):
                return Comparison.SAME

            return Comparison.MORE

        case [*left], int(right):
            if not left:
                return Comparison.LESS
            return check_pair((left, [right]))
        case int(left), [*right]:
            if not right:
                return Comparison.MORE
            return check_pair(([left], right))
        case int(left), int(right):
            if left < right:
                return Comparison.LESS
            elif left == right:
                return Comparison.SAME
            
            return Comparison.MORE
        case _:
            raise RuntimeError

def part1(data=test_data()):
    data = [row for row in data if row]
    it = iter(data)
    pairs = [(parse_list(x)[1], parse_list(next(it))[1]) for x in it]
    
    return sum(idx for idx, pair in enumerate(pairs, 1) if check_pair(pair) != Comparison.MORE)

import functools
def part2(data=test_data()):
    packets = [parse_list(row)[1] for row in data if row]
    packets.append([[6]])
    packets.append([[2]])

    sort_key = functools.cmp_to_key(lambda x, y: check_pair((x, y)).value)
    sorted_packets = sorted(packets, key=sort_key)
    return (sorted_packets.index([[6]]) + 1) * (sorted_packets.index([[2]]) + 1)

if __name__ == "__main__":
    print(part1())
    print(part1(get_data()))
    print(part2())
    print(part2(get_data()))