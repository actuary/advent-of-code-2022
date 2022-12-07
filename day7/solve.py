

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
        self.children = {}
        self.parent = None

    def add_node(self, child: "Node"):
        self.children[child.name] = child
        child.parent = self

    @property
    def is_dir(self) -> bool:
        return self.data == 0

    def __iter__(self):
        return iter(self.children.items())
    

def get_sizes(tree, size_dirs: dict) -> int:
    if tree == None:
        return 0

    if tree.is_dir:
        size = sum(get_sizes(child, size_dirs) for _, child in tree)
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
    dir_sizes = {}
    get_sizes(head, dir_sizes)
    return sum(size for size in dir_sizes.values() if size <= 100000)


def part2(data=test_data()):
    head = build_tree(data)
    dir_sizes = {}
    get_sizes(head, dir_sizes)

    root_dir_size = dir_sizes["/"] 
    threshold = 30000000 - (70000000 - root_dir_size)
    return min(value for value in dir_sizes.values() if value >= threshold)


if __name__ == "__main__":
    print(part1())
    print(part1(get_data()))
    print(part2())
    print(part2(get_data()))
