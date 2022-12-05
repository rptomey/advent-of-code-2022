import sys
import copy

example_stacks = {
    "1": ["N","Z"],
    "2": ["D","C","M"],
    "3": ["P"]
}

production_stacks = {
    "1": ["F","R","W"],
    "2": ["P","W","V","D","C","M","H","T"],
    "3": ["L","N","Z","M","P"],
    "4": ["R","H","C","J"],
    "5": ["B","T","Q","H","G","P","C"],
    "6": ["Z","F","L","W","C","G"],
    "7": ["C","G","J","Z","Q","L","V","W"],
    "8": ["C","V","T","W","F","R","N","P"],
    "9": ["V","S","R","G","H","W","J"]
}

def move_crates(stacks, quantity, from_stack, to_stack):
    while quantity > 0:
        active_crate = stacks[from_stack].pop(0)
        stacks[to_stack].insert(0,active_crate)
        quantity -= 1

def move_multiple_crates(stacks, quantity, from_stack, to_stack):
    active_crates = []
    while quantity > 0 and len(stacks[from_stack]) > 0:
        active_crates.append(stacks[from_stack].pop(0))
        quantity -= 1
    while len(active_crates) > 0:
        stacks[to_stack].insert(0,active_crates.pop())

def parse(file_name):
    """Parse input."""
    instructions = []
    
    with open(file_name) as f:
        for line in f:
            # Each line is like "move 2 from 4 to 9"
            contents = line.strip().split(" ")
            instruction = {
                "quantity": int(contents[1]),
                "from": contents[3],
                "to": contents[5]
            }
            instructions.append(instruction)

    return instructions

def part1(data, path):
    """Solve part 1."""
    these_stacks = {}
    if path == "example.txt":
        these_stacks = copy.deepcopy(example_stacks)
    elif path == "input.txt":
        these_stacks = copy.deepcopy(production_stacks)

    for instruction in data:
        move_crates(these_stacks, instruction["quantity"], instruction["from"], instruction["to"])

    stack_tops = []
    for key in these_stacks.keys():
        stack_tops.append(these_stacks[key][0])
    return "".join(stack_tops)

def part2(data, path):
    """Solve part 2."""
    those_stacks = {}
    if path == "example.txt":
        those_stacks = copy.deepcopy(example_stacks)
    elif path == "input.txt":
        those_stacks = copy.deepcopy(production_stacks)

    for instruction in data:
        move_multiple_crates(those_stacks, instruction["quantity"], instruction["from"], instruction["to"])
    stack_tops = []
    for key in those_stacks.keys():
        stack_tops.append(those_stacks[key][0])
    return "".join(stack_tops)

def solve(puzzle_input, path):
    """Solve the puzzle for the given input."""
    solution1 = part1(puzzle_input, path)
    solution2 = part2(puzzle_input, path)

    return solution1, solution2

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = parse(path)
        solutions = solve(puzzle_input, path)
        print("\n".join(str(solution) for solution in solutions))