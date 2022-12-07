from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

def get_data(filepath="input"):
    return open(filepath, "r").read().splitlines()


def test_data():
    return """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".splitlines()

class Node:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.size = data
        self.children = {}
        self.parent = None

    def add_node(self, child: "Node"):
        self.children[child.name] = child
        child.parent = self

    @property
    def is_dir(self) -> bool:
        return self.data == 0
    

def get_sizes(tree, size_dirs: dict, limit=70000000) -> int:
    if tree == None:
        return 0

    if tree.is_dir:
        size = sum(get_sizes(child, size_dirs, limit) 
                   for _, child in tree.children.items())
        if size <= limit:
            size_dirs[tree.name] = size
        return size
    return tree.data

def build_tree(data):
    head = Node("/", 0)
    tree = head
    for line in data[1:]:
        match line.split():
            case ["$", "cd", ".."]:
                if tree.parent:
                    tree = tree.parent
            case ["$", "cd", directory]:
                tree = tree.children[f"{tree.name}{directory}/"]
            case ["$", "ls"]:
                pass
            case ["dir", directory]:
                tree.add_node(Node(f"{tree.name}{directory}/", 0))
            case size, filename:
                tree.add_node(Node(f"{tree.name}{filename}", int(size)))
            case _:
                raise RuntimeError
    return head


def part1(data=test_data()):
    head = build_tree(data)
    small_dirs = {}
    get_sizes(head, small_dirs, 100000)
    return sum(small_dirs.values())


def part2(data=test_data()):
    head = build_tree(data)
    dirs = {}
    get_sizes(head, dirs)

    root_dir_size = dirs["/"] 
    unused_space = 70000000 - root_dir_size
    need_to_free_space = 30000000 - unused_space
    smallest_dir = 70000000
    for _, size in dirs.items():
        if size >= need_to_free_space and size <= smallest_dir:
            smallest_dir = size

    return smallest_dir



if __name__ == "__main__":
    print(part1())
    print(part1(get_data()))
    print(part2())
    print(part2(get_data()))
