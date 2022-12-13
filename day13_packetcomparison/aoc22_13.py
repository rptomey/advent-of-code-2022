import sys
import json

def compare(left, right):
    #print(f"- Compare {left} vs {right}")
    if type(left) == int and type(right) == int:
        if left < right:
            return 1
        elif left > right:
            return -1
        else:
            return 0
    
    # Make sure both sides are lists before we do anything else.
    if type(left) != list:
        left = [left]
    if type(right) != list:
        right = [right]

    # Check all of left against all of right.
    for i in range(len(left)):
        if i >= len(right):
            return -1
        result = compare(left[i], right[i])
        if result != 0:
            return result

    if len(left) < len(right):
        return 1
    elif len(left) > len(right):
        return -1
    else:
        return 0

def parse(file_name):
    """Parse input"""
    raw_input = []
    pairs = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                list_line = json.loads(clean_line)
                raw_input.append(list_line)

    input_count = len(raw_input)

    for i in range(0,input_count,2):
        pair = {
            "index": (i//2+1),
            "left": raw_input[i],
            "right": raw_input[i+1]
        }
        pairs.append(pair)
    
    return pairs

def part1(data):
    """Solve part 1."""
    ordered_pairs = 0
    for pair in data:
    #    print(f"== Pair {pair['index']} ==")
        left = pair["left"]
        right = pair["right"]
        result = compare(left, right)
    #    print(result)
        if result == 1:
            ordered_pairs += pair["index"]

    return ordered_pairs

def part2(data):
    """Solve part 2."""
    packets = []
    for pair in data:
        packets.append(pair["left"])
        packets.append(pair["right"])
    packets.append([[2]])
    packets.append([[6]])

    for i in range(len(packets)):
        for j in range(i+1,len(packets)):
            if compare(packets[i],packets[j]) == -1:
                packets[i], packets[j] = packets[j], packets[i]
                
    return (packets.index([[2]])+1) * (packets.index([[6]])+1)

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