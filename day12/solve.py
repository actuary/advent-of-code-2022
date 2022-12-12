from dataclasses import dataclass
from typing import Optional, Tuple
from collections import defaultdict
import sys
from queue import PriorityQueue

def get_data(filepath="input"):
    return open(filepath, "r").read().splitlines()


def test_data():
    return """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""".splitlines()
    

def make_graph(data):

    SENTINELS = {
        "S": "a",
        "E": "z"
    }
    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
  
    g = defaultdict(dict)
    source = None
    destination = None

    for y in range(len(data)):
        for x in range(len(data[y])):
            vertex = (y, x)
                
            
            if data[y][x] == "S":
                source = vertex
            elif data[y][x] == "E":
                destination = vertex

            value = SENTINELS.get(data[y][x], data[y][x])
            for direction in directions:
                dx, dy = direction
                new_x, new_y = x + dx, y + dy
                neighbour = (new_y, new_x)

                if 0 <= new_x < len(data[y]) and 0 <= new_y < len(data):
                    neighbour_value = data[new_y][new_x]
                    neighbour_value = SENTINELS.get(neighbour_value, neighbour_value)
                    distance = ord(neighbour_value) - ord(value)
                    if distance <= 1:
                        g[vertex][neighbour] = 1
    return g, source, destination


def shortest_path(g, source) -> Tuple[dict, dict]:
    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    visited = set()
    dist = {source: 0}
    prev = {}
    
    q = PriorityQueue()
    q.put((0, source))
    while not q.empty():
        _, u = q.get()
        while u in visited:
            _, u = q.get()

        visited.add(u)
        distance = dist[u]

        for v, v_distance in g[u].items():
            v_distance += distance
            if v not in visited and v_distance < dist.get(v, sys.maxsize):
                q.put((v_distance, v))
                dist[v] = v_distance
                prev[v] = u

    return dist, prev

        
def part1(data=test_data()):
    g, source, destination = make_graph(data)
    dist, _ = shortest_path(g, source)
    return dist[destination]


def part2(data=test_data()):
    g, _, destination = make_graph(data)
    
    starting_points = [vertex for vertex in g if data[vertex[0]][vertex[1]] in ("a", "S")]

    # v slow but no more thinking today
    return min(shortest_path(g, starting_point)[0][destination] 
               for starting_point in starting_points 
               if destination in shortest_path(g, starting_point)[0])


if __name__ == "__main__":
    print(part1())
    print(part1(get_data()))
    print(part2())
    print(part2(get_data()))
