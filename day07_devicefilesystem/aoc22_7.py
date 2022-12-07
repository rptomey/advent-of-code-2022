import sys
import re

def get_size_of_directory(filesystem, file_location):
    directory = filesystem[file_location]
    if directory["size"] == -1:
        file_sum = 0
        directory_sum = 0

        if "files" in directory.keys():
            for file in directory["files"]:
                file_sum += filesystem[file]["size"]

        if "child_directories" in directory.keys():
            for child_directory in directory["child_directories"]:
                directory_sum += get_size_of_directory(filesystem, child_directory)

        return file_sum + directory_sum
    else:
        return directory["size"]

def parse(file_name):
    """Parse input"""
    raw_input = []
    file_system = {}
    current_location = ""
    previous_location = ""

    # Feed the contents of the file into a list named "raw_input"
    with open(file_name) as f:
        for line in f:
            raw_input.append(line.strip())

    # Go through all input items
    for i in range(len(raw_input)):
        current_input = raw_input[i]
        input_portions = current_input.split()

        if input_portions[0] == "$":
            # If this is a change directory command, then update locations.
            if input_portions[1] == "cd":
                previous_location = current_location

                # Build the new current location based on new_dir.
                new_dir = input_portions[2]
                # Going to root first.
                if new_dir == "/":
                    current_location = "root"
                # Going to any other specific directory.
                elif new_dir != "..":
                    current_location = f"{current_location}/{new_dir}"
                # Going back up a level.
                else:
                    current_location = re.sub(r"\/[a-z\.]+$","", current_location)

                # Make sure the directory is in the file_system.
                if new_dir != ".." and current_location not in file_system.keys():
                    file_system[current_location] = {
                        "location": current_location,
                        "name": new_dir,
                        "parent": previous_location,
                        "type": "directory",
                        "size": -1
                    }
        # Next handle any listed directories.
        # Don't add them to the filesystem until we've checked them out,
        # but add them to the current locations child_directories.
        elif input_portions[0] == "dir":
            dir_path = f"{current_location}/{input_portions[1]}"
            if "child_directories" in file_system[current_location].keys():
                if dir_path not in file_system[current_location]["child_directories"]:
                    file_system[current_location]["child_directories"].append(dir_path)
            else:
                file_system[current_location]["child_directories"] = [dir_path]
        # Finally handle any listed files.
        else:
            file_size = input_portions[0]
            file_name = input_portions[1]
            file_location = f"{current_location}/{file_name}"
            # First add a reference to the current directory.
            if "files" in file_system[current_location].keys():
                if file_location not in file_system[current_location]["files"]:
                    file_system[current_location]["files"].append(file_location)
            else:
                file_system[current_location]["files"] = [file_location]
            # Then add the file to the file_system.
            if file_location not in file_system.keys():
                file_system[file_location] = {
                    "location": file_location,
                    "name": file_name,
                    "parent": current_location,
                    "type": "file",
                    "size": int(file_size)
                }
    for key in file_system.keys():
        if file_system[key]["type"] == "directory":
            file_system[key]["size"] = get_size_of_directory(file_system, key)

    return file_system

def part1(data):
    """Solve part 1."""
    sub_directory_total = 0

    for key in data.keys():
        if data[key]["type"] == "directory" and data[key]["size"] <= 100000:
            sub_directory_total += data[key]["size"]

    return sub_directory_total

def part2(data):
    """Solve part 2."""
    pass

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