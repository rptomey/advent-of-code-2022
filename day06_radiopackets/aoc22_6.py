import sys

def find_first_distinct_marker(packet, characters):
    for i in range(len(packet)):
        if len(set(packet[i:i+characters])) == characters:
            return i+characters

def parse(file_name):
    """Parse input."""
    packets = []
    
    with open(file_name) as f:
        for line in f:
            packets.append(line)

    return packets

def part1(data):
    """Solve part 1."""
    start_markers = []
    for packet in data:
        start_markers.append(find_first_distinct_marker(packet,4))

    return start_markers

def part2(data):
    """Solve part 2."""
    message_markers = []
    for packet in data:
        message_markers.append(find_first_distinct_marker(packet,14))

    return message_markers

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