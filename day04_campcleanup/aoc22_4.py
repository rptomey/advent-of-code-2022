import sys

def is_a_in_b(elf_a, elf_b):
    if elf_a["min"] >= elf_b["min"] and elf_a["max"] <= elf_b["max"]:
        return True
    else:
        return False

def does_a_overlap_b(elf_a, elf_b):
    if elf_a["min"] <= elf_b["min"] <= elf_a["max"]:
        return True
    elif elf_a["min"] <= elf_b["max"] <= elf_a["max"]:
        return True
    elif elf_b["min"] <= elf_a["min"] <= elf_b["max"]:
        return True
    elif elf_b["min"] <= elf_a["max"] <= elf_b["max"]:
        return True
    else:
        return False

def parse(file_name):
    """Parse input."""
    elf_pairs = []
    
    with open(file_name) as f:
        for line in f:
            pairing = line.split(",")
            elf_a = {
                "zone": pairing[0].strip(),
                "min": int(pairing[0].split("-")[0]),
                "max": int(pairing[0].split("-")[1])
            }
            elf_b = {
                "zone": pairing[1].strip(),
                "min": int(pairing[1].split("-")[0]),
                "max": int(pairing[1].split("-")[1])
            }
            elf_pair = [elf_a,elf_b]
            elf_pairs.append(elf_pair)

    return elf_pairs

def part1(data):
    """Solve part 1."""
    redundant_elves = 0
    for elf_pairing in data:
        if is_a_in_b(elf_pairing[0], elf_pairing[1]) or is_a_in_b(elf_pairing[1], elf_pairing[0]):
            redundant_elves += 1
            
    return redundant_elves

def part2(data):
    """Solve part 2."""
    overlapping_elves = 0
    for elf_pairing in data:
        if does_a_overlap_b(elf_pairing[0], elf_pairing[1]):
            overlapping_elves += 1

    return overlapping_elves

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