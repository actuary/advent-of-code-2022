from dataclasses import dataclass
from typing import Optional, Tuple

def get_data(filepath="input.txt"):
    return open(filepath, "r").read().splitlines()


def test_data():
    return """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""".splitlines()

@dataclass(frozen=True)
class Assignment:
    start: int
    end: int

    def to_set(self) -> set:
        return set(range(self.start, self.end+1))

    @staticmethod
    def from_id(id_str: str) -> "Assignment":
        start, end = id_str.split("-")
        return Assignment(int(start), int(end))


def intersect(assignment_a: Assignment, assignment_b: Assignment) -> Optional[Assignment]:
    if assignment_a.end < assignment_b.start:
        return None

    return Assignment(assignment_b.start, max(assignment_a.end, assignment_b.end))


def is_subset(assignment_a: Assignment, assignment_b: Assignment) -> bool:
    return assignment_a.start >= assignment_b.start and assignment_a.end <= assignment_b.end


def row_to_assignments(row: str) -> Tuple[Assignment, Assignment]:
    assignment_1, assignment_2 = tuple(Assignment.from_id(id_str) 
                                       for id_str in row.split(","))
    if assignment_1.start <= assignment_2.start:
        return assignment_1, assignment_2

    return assignment_2, assignment_1


def part1(data=test_data()):
    elf_pairs = (row_to_assignments(row) for row in data)

    return sum(is_subset(pair[0], pair[1]) or is_subset(pair[1], pair[0])
               for pair in elf_pairs)


def part2(data=test_data()):
    elf_pairs = (row_to_assignments(row) for row in data)

    return sum(intersect(pair[0], pair[1]) is not None 
               for pair in elf_pairs)

if __name__ == "__main__":
    print(part1())
    print(part1(get_data()))
    print(part2())
    print(part2(get_data()))
