from dataclasses import dataclass
from typing import Optional, Tuple

def get_data(filepath="input"):
    return open(filepath, "r").read().splitlines()


def test_data():
    return """30373
25512
65332
33549
35390""".splitlines()
# data[3][0] becomes data[0][1] i:=j, j:=5-i-1=5-3-1=1
# data[2][2] becomes data[2][2] i:=2, j:=5-2-1=2
# data[3][3] becomes data[3][1] i:=3, j:=5-3-1=1

import itertools
from typing import Iterable

def get_accum_max(lst: Iterable) -> Iterable:
    return "".join(list(itertools.accumulate(lst, lambda a, b: max(a, b))))

def part1(data=test_data()):
    maxes = [[get_accum_max(row) for row in data],
            [get_accum_max(reversed(row))[::-1] for row in data]
        ]  

    transposed = list(zip(*data))
    maxes.append([get_accum_max(row) for row in transposed])
    maxes.append([get_accum_max(reversed(row))[::-1] for row in transposed])
    maxes = list(zip(*maxes))

    result = len(data) * len(data[0]) - (len(data)-2)*(len(data[0]) - 2)
    result += sum(data[i][j] > min(maxes[i][0][j-1], 
                               maxes[i][1][j+1], 
                               maxes[j][2][i-1], 
                               maxes[j][3][i+1]) 
                   for i in range(1, len(data)-1) 
                   for j in range(1, len(data[i])-1))
    return result

def get_view_distances(data):
    number_of_cols = len(data[0])
    number_of_rows = len(data)
    view_distances = [[0]*len(row) for row in data] 
    for i in range(1, number_of_rows-1):
        for j in range(1, number_of_cols):
            view_distance = 0
            k = j - 1
            while k >= 0 and data[i][j] > data[i][k]:
                k -= 1
                view_distance += 1
            view_distance += (k >= 0)

            view_distances[i][j] = view_distance
    return view_distances

def part2(data=test_data()):
    left = get_view_distances(data)
    right = get_view_distances([row[::-1] for row in data])
    up = get_view_distances(["".join(x) for x in list(zip(*data))])
    down = get_view_distances([row[::-1] for row in ["".join(x) for x in list(zip(*data))]])

    scenic_scores = [[0]*len(row) for row in data] 
    for i in range(1, len(data)):
        for j in range(1, len(data)):
            scenic_scores[i][j] = (
                    left[i][j] 
                  * right[i][len(data[0])-j-1] 
                  * up[j][i] 
                  * down[j][len(data)-i-1]
            )
            

    return max(max(row) for row in scenic_scores)

if __name__ == "__main__":
    print(part1())
    print(part1(get_data()))
    print(part2())
    print(part2(get_data()))

