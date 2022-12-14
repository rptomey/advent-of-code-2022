import sys
import copy

def parse(file_name):
    """Parse input"""
    raw_input = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                raw_input.append(clean_line)

    drawing_instructions = []

    for item in raw_input:
        coordinates = item.split(" -> ")
        for i in range(len(coordinates)-1):
            from_point = coordinates[i]
            from_x = from_point.split(",")[0]
            from_y = from_point.split(",")[1]
            to_point = coordinates[i+1]
            to_x = to_point.split(",")[0]
            to_y = to_point.split(",")[1]
            instruction = {
                "from_x": int(from_x),
                "from_y": int(from_y),
                "to_x": int(to_x),
                "to_y": int(to_y)
            }
            drawing_instructions.append(instruction)

    cave = {
        "lowest_y": 0
    }
    
    for instruction in drawing_instructions:
        from_x = instruction["from_x"]
        from_y = instruction["from_y"]
        to_x = instruction["to_x"]
        to_y = instruction["to_y"]
        # Keep track of how low the rocks go
        if from_y > cave["lowest_y"]:
            cave["lowest_y"] = from_y
        if to_y > cave["lowest_y"]:
            cave["lowest_y"] = to_y
        # Draw a vertical line...
        if from_x == to_x and from_y != to_y:
            # ...going up.
            if from_y < to_y:
                for i in range(from_y, to_y+1):
                    cave[f"{from_x},{i}"] = {
                        "coordinate": f"{from_x},{i}",
                        "type": "rock"
                    }
            # ...going down.
            elif from_y > to_y:
                for i in range(to_y, from_y+1):
                    cave[f"{from_x},{i}"] = {
                        "coordinate": f"{from_x},{i}",
                        "type": "rock"
                    }
        # Draw a horizontal line...
        if from_x != to_x and from_y == to_y:
            # ...going right.
            if from_x < to_x:
                for i in range(from_x, to_x+1):
                    cave[f"{i},{from_y}"] = {
                        "coordinate": f"{i},{from_y}",
                        "type": "rock"
                    }
            # ...going left.
            elif from_x > to_x:
                for i in range(to_x, from_x+1):
                    cave[f"{i},{from_y}"] = {
                        "coordinate": f"{i},{from_y}",
                        "type": "rock"
                    }
    
    return cave

def part1(data):
    """Solve part 1."""
    data = copy.deepcopy(data)
    sand_count = 0
    lowest_y = data["lowest_y"]
    lowest_reached = False
    while lowest_reached == False:
        # Temporary pointer
        x = 500
        y = 0
        spaces_available = True
        while spaces_available == True:
            # print(f"Checking based on coordinate {x},{y}")
            # Sand tries to move down first...
            if f"{x},{y+1}" not in data.keys():
                y += 1
            # ...then diagonally left...
            elif f"{x-1},{y+1}" not in data.keys():
                x -= 1
                y += 1
            # ...then diagonally right...
            elif f"{x+1},{y+1}" not in data.keys():
                x += 1
                y += 1
            # ...or stops.
            else:
                spaces_available = False

            # Before we loop again or place a sand, make sure we haven't reached the lowest point.
            if y == lowest_y:
                lowest_reached = True
                spaces_available = False
            
            # If we're out of space, place the sand before looping the outer loop.
            elif spaces_available == False:
                data[f"{x},{y}"] = {
                    "coordinate": f"{x},{y}",
                    "type": "sand"
                }
                sand_count += 1
    
    return sand_count

def part2(data):
    """Solve part 2."""
    
    data = copy.deepcopy(data)
    sand_count = 0
    floor = data["lowest_y"] + 2
    
    while f"{500},{0}" not in data.keys():
        # Temporary pointer
        x = 500
        y = 0
        spaces_available = True
        while spaces_available == True:
            # print(f"Checking based on coordinate {x},{y}")
            # Before checking all directions down, see if we've reached the floor.
            if y + 1 == floor:
                spaces_available = False
            # Next, sand tries to move down first...
            elif f"{x},{y+1}" not in data.keys():
                y += 1
            # ...then diagonally left...
            elif f"{x-1},{y+1}" not in data.keys():
                x -= 1
                y += 1
            # ...then diagonally right...
            elif f"{x+1},{y+1}" not in data.keys():
                x += 1
                y += 1
            # ...or stops.
            else:
                spaces_available = False
            
            # If we're out of space, place the sand before looping the outer loop.
            if spaces_available == False:
                data[f"{x},{y}"] = {
                    "coordinate": f"{x},{y}",
                    "type": "sand"
                }
                sand_count += 1
    
    return sand_count

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