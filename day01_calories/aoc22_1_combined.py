import sys

def parse(file_name):
    """Parse input."""
    elves = []
    current_elf = 0
    
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                current_elf += int(line)
            else:
                elves.append(current_elf)
                current_elf = 0

    # Get the last elf in there, too, since there's not a blank line at the end of the input...
    elves.append(current_elf)
    
    # Sort the list and return it.
    return sorted(elves, reverse=True)

def part1(data):
    """Solve part 1."""
    return data[0]

def part2(data):
    """Solve part 2."""
    return sum(data[0:3])

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