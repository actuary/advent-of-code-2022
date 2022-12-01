
def solve(data):
    return max([sum([int(calories) for calories in elf.split("\n") if calories]) 
                                   for elf in data.split("\n\n")])

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        data = f.read()

    print(solve(data))
