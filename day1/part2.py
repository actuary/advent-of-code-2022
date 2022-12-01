
def solve(data):
    return sum(sorted([sum([int(calories) for calories in elf.split("\n") if calories]) 
        for elf in data.split("\n\n")], reverse=True)[:3])

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        data = f.read()

    print(solve(data))
