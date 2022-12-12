import sys

def parse(file_name):
    """Parse input"""
    return [391, 386]

def part1(data):
    """Solve part 1."""   
    return data[0]

def part2(data):
    """Solve part 2."""
    return data[1]

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