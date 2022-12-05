import sys
import re

def letter_priority(letter):
    if re.match("[a-z]", letter):
        return ord(letter) - 96
    elif re.match("[A-Z]", letter):
        return ord(letter) - 38
    else:
        return 0

def parse(file_name):
    """Parse input."""
    backpacks = []
    
    with open(file_name) as f:
        for line in f:
            parcel_size = int(len(line) / 2)
            parcel_1 = line[0:parcel_size]
            parcel_2 = line[parcel_size:]
            backpack = {
                "full_pack": line.strip(),
                "parcel_1": parcel_1,
                "parcel_2": parcel_2
            }
            backpacks.append(backpack)

    return backpacks

def part1(data):
    """Solve part 1."""
    priority_total = 0
    for backpack in data:
        unique_items = list(set(backpack["parcel_1"]))
        for letter in unique_items:
            if letter in backpack["parcel_2"]:
                priority_total += letter_priority(letter)
    return priority_total

def part2(data):
    """Solve part 2."""
    badge_total = 0
    backback_count = len(data)
    groups = []
    
    for i in range(0,backback_count,3):
        groups.append(data[i:i+3])
    
    for group in groups:
        unique_items = list(set(group[0]["full_pack"]))
        for letter in unique_items:
            if letter in group[1]["full_pack"] and letter in group[2]["full_pack"]:
                badge_total += letter_priority(letter)
                break

    return badge_total

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    solution1 = part1(puzzle_input)
    solution2 = part2(puzzle_input)

    return solution1, solution2

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = parse(path)
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))