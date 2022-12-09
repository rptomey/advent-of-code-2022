import sys

def move_vertical(knot, change):
    current_y = knot["pos_y"]
    knot["pos_y"] = current_y + change
    update_history(knot)

def move_horizontal(knot, change):
    current_x = knot["pos_x"]
    knot["pos_x"] = current_x + change
    update_history(knot)

def move_diagonal(knot, change_x, change_y):
    current_x = knot["pos_x"]
    current_y = knot["pos_y"]
    knot["pos_x"] = current_x + change_x
    knot["pos_y"] = current_y + change_y
    update_history(knot)

def update_history(knot):
    knot["history"].append(f"{knot['pos_x']},{knot['pos_y']}")

def evaluate_following_movement(lead_knot, following_knot):
    # If they're in the same x row, but y is greater than 1 away, move up or down.
    if following_knot["pos_x"] == lead_knot["pos_x"] and following_knot["pos_y"] != lead_knot["pos_y"]:
        if following_knot["pos_y"] < lead_knot["pos_y"] and lead_knot["pos_y"] - following_knot["pos_y"] > 1:
            move_vertical(following_knot, 1)
        elif following_knot["pos_y"] > lead_knot["pos_y"] and following_knot["pos_y"] - lead_knot["pos_y"] > 1:
            move_vertical(following_knot, -1)
    # And if they're in the same y row, but x is greater than 1 away, move right or left.
    elif following_knot["pos_x"] != lead_knot["pos_x"] and following_knot["pos_y"] == lead_knot["pos_y"]:
        if following_knot["pos_x"] < lead_knot["pos_x"] and lead_knot["pos_x"] - following_knot["pos_x"] > 1:
            move_horizontal(following_knot, 1)
        elif following_knot["pos_x"] > lead_knot["pos_x"] and following_knot["pos_x"] - lead_knot["pos_x"] > 1:
            move_horizontal(following_knot, -1)
    # And if neither rows are the same, move diagonally.
    elif following_knot["pos_x"] != lead_knot["pos_x"] and following_knot["pos_y"] != lead_knot["pos_y"]:
        if following_knot["pos_x"] < lead_knot["pos_x"] and following_knot["pos_y"] < lead_knot["pos_y"]:
            if lead_knot["pos_x"] - following_knot["pos_x"] > 1 or lead_knot["pos_y"] - following_knot["pos_y"] > 1:
                move_diagonal(following_knot, 1, 1)
        elif following_knot["pos_x"] > lead_knot["pos_x"] and following_knot["pos_y"] < lead_knot["pos_y"]:
            if following_knot["pos_x"] - lead_knot["pos_x"] > 1 or lead_knot["pos_y"] - following_knot["pos_y"] > 1:
                move_diagonal(following_knot, -1, 1)
        elif following_knot["pos_x"] < lead_knot["pos_x"] and following_knot["pos_y"] > lead_knot["pos_y"]:
            if lead_knot["pos_x"] - following_knot["pos_x"] > 1 or following_knot["pos_y"] - lead_knot["pos_y"] > 1:
                move_diagonal(following_knot, 1, -1)
        elif following_knot["pos_x"] > lead_knot["pos_x"] and following_knot["pos_y"] > lead_knot["pos_y"]:
            if following_knot["pos_x"] - lead_knot["pos_x"] > 1 or following_knot["pos_y"] - lead_knot["pos_y"] > 1:
                move_diagonal(following_knot, -1, -1)

def parse(file_name):
    """Parse input"""
    instructions = []

    # Each row is like "U 23", which would mean "go up 23 positions".
    with open(file_name) as f:
        for line in f:
            instruction_pair = line.strip().split()
            instruction = {
                "direction": instruction_pair[0],
                "distance": int(instruction_pair[1])
            }
            instructions.append(instruction)

    return instructions

def part1(data):
    """Solve part 1."""
    # Initialize the head end of the rope.
    head = {
        "pos_x": 0,
        "pos_y": 0,
        "history": ["0,0"]
    }
    
    # Initialize the tail end of the rope.
    tail = {
        "pos_x": 0,
        "pos_y": 0,
        "history": ["0,0"]
    }

    # Follow the instructions.
    for instruction in data:
        # Both ends move at the same time, so we can't just move one then the other.
        distance = instruction["distance"]
        while distance > 0:
            distance -= 1
            # Move the head first because it's just based on the instruction.
            match instruction["direction"]:
                case "U":
                    move_vertical(head, 1)
                case "D":
                    move_vertical(head, -1)
                case "L":
                    move_horizontal(head, -1)
                case "R":
                    move_horizontal(head, 1)
            # Move the tail next based on where the head is...
            evaluate_following_movement(head, tail)

    # print(tail["history"])
    # print(set(tail["history"]))
    return len(set(tail["history"]))

def part2(data):
    """Solve part 2."""
    # Initialize the whole rope with 10 knots, with 0 being head and 9 being tail.
    rope = {}
    for i in range(10):
        rope[i] = {
            "pos_x": 0,
            "pos_y": 0,
            "history": ["0,0"]
        }

    # Again, follow the instructions.
    for instruction in data:
        distance = instruction["distance"]
        while distance > 0:
            distance -= 1
            # Head still moves normally, but it's just called rope[0].
            match instruction["direction"]:
                case "U":
                    move_vertical(rope[0], 1)
                case "D":
                    move_vertical(rope[0], -1)
                case "L":
                    move_horizontal(rope[0], -1)
                case "R":
                    move_horizontal(rope[0], 1)
            # The rest of the rope will move 1 knot at a time.
            for i in range(1,10):
                evaluate_following_movement(rope[i-1], rope[i])
    
    # print(rope[9]["history"])
    return len(set(rope[9]["history"]))            

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