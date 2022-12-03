

def get_data(filepath="input.txt"):
    return open(filepath, "r").read().splitlines()


def test_data():
    return """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""".splitlines()


def split_rucksacks(data):
    return [(set(row[:int(len(row)/2)]), set(row[int(len(row)/2):]))
            for row in data if row]


def score_item(item):
    return ord(item.lower()) - ord('a') + 1 + 26 * item.isupper()


def part1(data=test_data()):
    rucksacks = split_rucksacks(data)
    common_items = [(left & right) for (left, right) in rucksacks]

    return sum(score_item(items.pop()) for items in common_items)


def part2(data):
    GROUP_SIZE = 3
    elf_groups = [(set(elf) for elf in group)
                  for group in zip(*[iter(data)] * GROUP_SIZE)]

    return sum(score_item(set.intersection(*group).pop()) for group in elf_groups)



if __name__ == "__main__":
    print(part1(test_data()))
    print(part1(get_data()))
    print(part2(test_data()))
    print(part2(get_data()))
