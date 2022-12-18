from dataclasses import dataclass
from typing import Optional, Tuple, List, Set
from collections import defaultdict
import sys
import re


def get_data(filepath="input"):
    return open(filepath, "r").read().splitlines()


def test_data():
    return """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3""".splitlines()


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)
    
    def __gt__(self, other: "Position") -> bool:
        return self.x > other.x

    def __gte__(self, other: "Position") -> bool:
        return self.x >= other.x

    def __lt__(self, other: "Position") -> bool:
        return self.x < other.x

    def __lte__(self, other: "Position") -> bool:
        return self.x <= other.x

    def __eq__(self, other: "Position") -> bool:
        return self.x == other.x


@dataclass(frozen=True)
class LineSegment:
    start: Position
    end: Position

    def __len__(self) -> int:
        return self.end.x - self.start.x + 1


@dataclass
class Sensor:
    pos: Position
    closest_beacon: Position

    def radius(self) -> int:
        return manhattan_dist(self.pos, self.closest_beacon)

    def perimeter(self) -> List[Position]:
        radius = self.radius()
        return [
            Position(self.pos.x, self.pos.y + radius),
            Position(self.pos.x + radius, self.pos.y),
            Position(self.pos.x, self.pos.y - radius),
            Position(self.pos.x - radius, self.pos.y),
        ]
        

REGEX = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): "
                   r"closest beacon is at x=(-?\d+), y=(-?\d+)")


def parse_sensor(line) -> Sensor:
    m = REGEX.match(line)
    if not m:
        raise RuntimeError

    return Sensor(Position(int(m.group(1)), int(m.group(2))), 
                  Position(int(m.group(3)), int(m.group(4))))


def manhattan_dist(from_pos: Position, to_pos: Position):
    return abs(to_pos.y - from_pos.y) + abs(to_pos.x - from_pos.x)


def intersect_line(sensor: Sensor, y: int) -> Optional[LineSegment]:
    y_dist = abs(y - sensor.pos.y)
    line_radius = (sensor.radius() - y_dist)

    if line_radius <= 0:
        return None

    return LineSegment(Position(sensor.pos.x - line_radius, y), 
                       Position(sensor.pos.x + line_radius, y))


def cap_line_segment(segment, start, stop) -> LineSegment:
    return LineSegment(Position(min(max(segment.start.x, start), stop), segment.start.y),
                       Position(min(max(segment.end.x, start), stop), segment.end.y))


def disjoint_line_segments(segments: list, y: int, start=-sys.maxsize, stop=sys.maxsize):
    min_x, max_x = None, None
    result_segments = set()

    while len(segments) > 0:
        segment = segments.pop(0)
        segment = cap_line_segment(segment, start, stop)

        if min_x is None or max_x is None:
            min_x, max_x = segment.start.x, segment.end.x

        if segment.start.x > max_x:
            new_segment = LineSegment(Position(min_x, y), Position(max_x, y))
            result_segments.add(new_segment)
            min_x, max_x = segment.start.x, segment.end.x
        else:
            max_x = max(max_x, segment.end.x)

    if min_x is not None and max_x is not None:
        result_segments.add(LineSegment(Position(min_x, y), Position(max_x, y)))

    return result_segments


def part1(data=test_data(), y=10):
    sensors = [parse_sensor(line) for line in data]

    segments = [intersect_line(sensor, y) for sensor in sensors]
    segments = [segment for segment in segments if segment]
    segments = sorted(segments, key=lambda segment: segment.start.x)
    segments = disjoint_line_segments(segments, y)
    
    beacons = set(sensor.closest_beacon for sensor in sensors)
    number_of_beacons = sum([beacon.y == y for beacon in beacons])

    return sum(len(segment) for segment in segments) - number_of_beacons


def part2(data=test_data(), start=0, stop=4000000):
    # takes a minute, spits out two line segments that have a size
    # 1 gap then just solved it using a calculator
    sensors = [parse_sensor(line) for line in data]

    for y in range(stop+1):
        segments = [intersect_line(sensor, y) for sensor in sensors]
        segments = [segment for segment in segments if segment]
        segments = sorted(segments, key=lambda segment: segment.start.x)
        segments = disjoint_line_segments(segments, y, start, stop)

        if sum(len(segment) for segment in segments) < stop + 1:
            return segments

    return None


if __name__ == "__main__":
    print(part1(y=10))
    print(part1(get_data(), y=2000000))
    print(part2(start=0, stop=20))
    print(part2(get_data()))
