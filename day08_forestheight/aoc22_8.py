import sys

def parse(file_name):
    """Parse input"""
    forest = []

    # Feed the contents as rows of trees into forest.
    with open(file_name) as f:
        for line in f:
            tree_row = []
            for char in line:
                if char != "\n":
                    tree = {
                        "height": int(char),
                        "visible": False
                    }
                    tree_row.append(tree)
            forest.append(tree_row)

    return forest

def part1(data):
    """Solve part 1."""
    forest_size = len(data)

    for x in range(forest_size):
        max_height_seen = -1
        for y in range(forest_size):
            if max_height_seen == 9:
                break
            elif data[x][y]["height"] > max_height_seen:
                data[x][y]["visible"] = True
                max_height_seen = data[x][y]["height"]

    for y in range(forest_size):
        max_height_seen = -1
        for x in range(forest_size):
            if max_height_seen == 9:
                break
            elif data[x][y]["height"] > max_height_seen:
                data[x][y]["visible"] = True
                max_height_seen = data[x][y]["height"]

    for x in range(forest_size-1, -1, -1):
        max_height_seen = -1
        for y in range(forest_size-1, -1, -1):
            if max_height_seen == 9:
                break
            elif data[x][y]["height"] > max_height_seen:
                data[x][y]["visible"] = True
                max_height_seen = data[x][y]["height"]

    for y in range(forest_size-1, -1, -1):
        max_height_seen = -1
        for x in range(forest_size-1, -1, -1):
            if max_height_seen == 9:
                break
            elif data[x][y]["height"] > max_height_seen:
                data[x][y]["visible"] = True
                max_height_seen = data[x][y]["height"]

    visible_trees = 0

    for x in range(forest_size):
        for y in range(forest_size):
            if data[x][y]["visible"] == True:
                visible_trees += 1

    return visible_trees                

def part2(data):
    """Solve part 2."""
    forest_size = len(data)
    max_scenic_score = -1

    # Check every tree
    for x in range(forest_size):
        for y in range(forest_size):
            tree_height = data[x][y]["height"]
            # Look in direction 1
            viz_1 = 0
            for i in range(x+1, forest_size):
                if data[i][y]["height"] < tree_height:
                    viz_1 += 1
                else:
                    viz_1 += 1
                    break
            # Look in direction 2
            viz_2 = 0
            for i in range(y+1, forest_size):
                if data[x][i]["height"] < tree_height:
                    viz_2 += 1
                else:
                    viz_2 += 1
                    break
            # Look in direction 3
            viz_3 = 0
            for i in range(x-1, -1, -1):
                if data[i][y]["height"] < tree_height:
                    viz_3 += 1
                else:
                    viz_3 += 1
                    break
            # Look in direction 4
            viz_4 = 0
            for i in range(y-1, -1, -1):
                if data[x][i]["height"] < tree_height:
                    viz_4 += 1
                else:
                    viz_4 += 1
                    break
            # Calculate scenic score
            scenic_score = viz_1 * viz_2 * viz_3 * viz_4
            # Update max scenic score so we don't have to test everything again
            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score

    return max_scenic_score     

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