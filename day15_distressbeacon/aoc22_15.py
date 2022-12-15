import sys
import re
import copy

def find_top_from_ahead(s_x, b_x, b_y):
    while b_x > s_x:
        b_x -= 1
        b_y += 1
    return b_y

def find_right_from_above(s_y, b_x, b_y):
    while b_y > s_y:
        b_y -= 1
        b_x += 1
    return b_x

def find_bottom_from_ahead(s_x, b_x, b_y):
    while b_x > s_x:
        b_x -= 1
        b_y -= 1
    return b_y

def find_right_from_below(s_y, b_x, b_y):
    while b_y < s_y:
        b_y += 1
        b_x += 1
    return b_x

def find_left_from_below(s_y, b_x, b_y):
    while b_y < s_y:
        b_y += 1
        b_x -= 1
    return b_x

def find_bottom_from_behind(s_x, b_x, b_y):
    while b_x < s_x:
        b_x += 1
        b_y -= 1
    return b_y

def find_top_from_behind(s_x, b_x, b_y):
    while b_x < s_x:
        b_x += 1
        b_y += 1
    return b_y

def find_left_from_above(s_y, b_x, b_y):
    while b_y > s_y:
        b_y -= 1
        b_x -= 1
    return b_x

def parse(file_name):
    """Parse input"""
    sensors = []

    # First just get the sensors and the beacons they see.
    with open(file_name) as f:
        for line in f:
            # Example: "Sensor at x=3897, y=2076376: closest beacon is at x=-266803, y=2440278"
            coord_strings = re.findall(r"\-?[0-9]+", line)
            coord_ints = [int(x) for x in coord_strings]
            sensor = {
                "sensor_loc": (coord_ints[0], coord_ints[1]),
                "s_x": coord_ints[0],
                "s_y": coord_ints[1],
                "closest_beacon_loc": (coord_ints[2], coord_ints[3]),
                "b_x": coord_ints[2],
                "b_y": coord_ints[3],
            }
            sensors.append(sensor)

    # Then calculate the max and min x,y coordinates for each sensor for calculating where the void exists.
    for sensor in sensors:
        s_x = sensor["s_x"]
        s_y = sensor["s_y"]
        b_x = sensor["b_x"]
        b_y = sensor["b_y"]
        # Handle all 8 relative possible positions: U, UR, R, DR, D, DL, L, UL
        # U
        if b_y > s_y and b_x == s_x:
            top = b_y
            sensor["max_y"] = top
            sensor["min_y"] = top - (top - s_y) * 2
            right = find_right_from_above(s_y, b_x, b_y)
            sensor["max_x"] = right
            sensor["min_x"] = right - (right - s_x) * 2
        # UR
        elif b_y > s_y and b_x > s_x:
            top = find_top_from_ahead(s_x, b_x, b_y)
            sensor["max_y"] = top
            sensor["min_y"] = top - (top - s_y) * 2
            right = find_right_from_above(s_y, b_x, b_y)
            sensor["max_x"] = right
            sensor["min_x"] = right - (right - s_x) * 2
        # R
        elif b_y == s_y and b_x > s_x:
            top = find_top_from_ahead(s_x, b_x, b_y)
            sensor["max_y"] = top
            sensor["min_y"] = top - (top - s_y) * 2
            right = b_x
            sensor["max_x"] = right
            sensor["min_x"] = right - (right - s_x) * 2
        # DR
        elif b_y < s_y and b_x > s_x:
            bottom = find_bottom_from_ahead(s_x, b_x, b_y)
            sensor["min_y"] = bottom
            sensor["max_y"] = s_y + (s_y - bottom)
            right = find_right_from_below(s_y, b_x, b_y)
            sensor["max_x"] = right
            sensor["min_x"] = right - (right - s_x) * 2
        # D
        elif b_y < s_y and b_x == s_x:
            bottom = b_y
            sensor["min_y"] = bottom
            sensor["max_y"] = s_y + (s_y - bottom)
            left = find_left_from_below(s_y, b_x, b_y)
            sensor["min_x"] = left
            sensor["max_x"] = s_x + (s_x - left)
        # DL
        elif b_y < s_y and b_x < s_x:
            bottom = find_bottom_from_behind(s_x, b_x, b_y)
            sensor["min_y"] = bottom
            sensor["max_y"] = s_y + (s_y - bottom)
            left = find_left_from_below(s_y, b_x, b_y)
            sensor["min_x"] = left
            sensor["max_x"] = s_x + (s_x - left)
        # L
        elif b_y == s_y and b_x < s_x:
            top = find_top_from_behind(s_x, b_x, b_y)
            sensor["max_y"] = top
            sensor["min_y"] = top - (top - s_y) * 2
            left = b_x
            sensor["min_x"] = left
            sensor["max_x"] = s_x + (s_x - left)
        # UL
        elif b_y > s_y and b_x < s_x:
            top = find_top_from_behind(s_x, b_x, b_y)
            sensor["max_y"] = top
            sensor["min_y"] = top - (top - s_y) * 2
            left = find_left_from_above(s_y, b_x, b_y)
            sensor["min_x"] = left
            sensor["max_x"] = s_x + (s_x - left)
    
    return sensors

def part1(data):
    """Solve part 1."""
    check_y = 2000000

    # Make sure we're not wasting time on sensors that didn't scan the check_y row.
    relevant_sensors = []
    for sensor in data:
        if sensor["min_y"] <= check_y <= sensor["max_y"]:
            relevant_sensors.append(sensor)

    # Make sure we're not counting any beacons as void space
    parallel_beacon_x_values = set()
    for sensor in relevant_sensors:
        if sensor["b_y"] == check_y:
            parallel_beacon_x_values.add(sensor["b_x"])

    # Figure out which x values on the y axis are void spaces
    void_x_values = set()
    for sensor in relevant_sensors:
        # There are 5 possible relative positions when comparing check_y to sensor y, with varying complexities: top, above, parallel, below, bottom
        # top
        if sensor["max_y"] == check_y:
            if sensor["s_x"] not in parallel_beacon_x_values:
                void_x_values.add(sensor["s_x"])
        # above
        elif sensor["s_y"] < check_y < sensor["max_y"]:
            # Find the top-right from a pointer at the top
            p_y = sensor["max_y"]
            p_x = sensor["s_x"]
            while p_y > check_y:
                p_y -= 1
                p_x += 1
            right_x = p_x
            left_x = right_x - (right_x - sensor["s_x"]) * 2
            for i in range(left_x, right_x+1):
                if i not in parallel_beacon_x_values:
                    void_x_values.add(i)
        # parallel
        elif sensor["s_y"] == check_y:
            for i in range(sensor["min_x"], sensor["max_x"]+1):
                if i not in parallel_beacon_x_values:
                    void_x_values.add(i)
        # below
        elif sensor["s_y"] > check_y > sensor["min_y"]:
            # Find the bottom-right from a pointer at the bottom
            p_y = sensor["min_y"]
            p_x = sensor["s_x"]
            while p_y < check_y:
                p_y += 1
                p_x += 1
            right_x = p_x
            left_x = right_x - (right_x - sensor["s_x"]) * 2
            for i in range(left_x, right_x+1):
                if i not in parallel_beacon_x_values:
                    void_x_values.add(i)
        # bottom
        elif sensor["min_y"] == check_y:
            if sensor["s_x"] not in parallel_beacon_x_values:
                void_x_values.add(sensor["s_x"])

    return len(void_x_values)

def part2(data):
    """Solve part 2."""
    area_boundary = 4000000

    # Make sure we're not wasting time on completely wrong sensors (some may not overlap but whatever)
    relevant_sensors = []
    for sensor in data:
        # sensor has horizontal overlap
        if 0 <= sensor["min_x"] <= area_boundary or 0 <= sensor["max_x"] <= area_boundary:
            relevant_sensors.append(sensor)
        # sensor has vertical overlap
        elif 0 <= sensor["min_y"] <= area_boundary or 0 <= sensor["max_y"] <= area_boundary:
            relevant_sensors.append(sensor)

    # Find the relevant border of each sensor
    for sensor in relevant_sensors:
        print(f"Plotting border of sensor {sensor['sensor_loc']}")
        sensor["border"] = []
        for y in range(sensor["min_y"], sensor["max_y"]+1):
            if 0 <= y <= area_boundary:
                if y == sensor["min_y"]:
                    point = (sensor["s_x"],y)
                    if 0 <= point[0] <= area_boundary:
                        sensor["border"].append(point)
                elif y < sensor["s_y"]:
                    distance_from_bottom = y - sensor["min_y"]
                    center = sensor["s_x"]
                    left_point = (center-distance_from_bottom, y)
                    right_point = (center+distance_from_bottom, y)
                    if 0 <= left_point[0] <= area_boundary:
                        sensor["border"].append(left_point)
                    if 0 <= right_point[0] <= area_boundary:
                        sensor["border"].append(right_point)
                elif y == sensor["s_y"]:
                    left_point = (sensor["min_x"], y)
                    right_point = (sensor["max_x"], y)
                    if 0 <= left_point[0] <= area_boundary:
                        sensor["border"].append(left_point)
                    if 0 <= right_point[0] <= area_boundary:
                        sensor["border"].append(right_point)
                elif y > sensor["s_y"]:
                    distance_from_top = sensor["max_y"] - y
                    center = sensor["s_x"]
                    left_point = (center-distance_from_top, y)
                    right_point = (center+distance_from_top, y)
                    if 0 <= left_point[0] <= area_boundary:
                        sensor["border"].append(left_point)
                    if 0 <= right_point[0] <= area_boundary:
                        sensor["border"].append(right_point)
                elif y == sensor["max_y"]:
                    point = (sensor["s_x"], y)
                    if 0 <= point[0] <= area_boundary:
                        sensor["border"].append(point)
    num_sensors = len(relevant_sensors)
    checked_sensors = 0
    possible_spaces_horizontal = set()
    possible_spaces_vertical = set()
    # For each combination of sensors, see if any two border points are exactly 2 apart, vertically or horizontally.
    for sensor_a in relevant_sensors:
        checked_sensors += 1
        for sensor_b in relevant_sensors:
            print(f"Checking sensor {sensor_a['sensor_loc']} against {sensor_b['sensor_loc']} - ({checked_sensors} of {num_sensors})")
            a_manhattan = abs(sensor_a["b_x"] - sensor_a["s_x"]) + abs(sensor_a["b_y"] - sensor_a["s_y"])
            b_manhattan = abs(sensor_b["b_x"] - sensor_b["s_x"]) + abs(sensor_b["b_y"] - sensor_b["s_y"])
            ab_manhattan = abs(sensor_b["s_x"] - sensor_a["s_x"]) + abs(sensor_b["s_y"] - sensor_a["s_y"])
            if a_manhattan + b_manhattan < ab_manhattan:
                a_border = len(sensor_a["border"])
                checked_borders = 0
                for space_a in sensor_a["border"]:
                    checked_borders += 1
                    print(f"Checking border {checked_borders} of {a_border}")
                    for space_b in sensor_b["border"]:
                        if space_b[0] - space_a[0] == 2 and space_b[1] == space_a[1]:
                            point = (space_b[0]-1, space_b[1])
                            possible_spaces_horizontal.add(point)
                        if space_b[1] - space_a[1] == 2 and space_b[0] == space_a[0]:
                            point = (space_b[0], space_b[1]-1)
                            possible_spaces_vertical.add(point)
    
    overlapping_spaces = set()
    # Narrow down to only spaces from both
    for space in possible_spaces_horizontal:
        if space in possible_spaces_vertical:
            overlapping_spaces.add(space)

    # Compare the Manhattan distance of each remaining space to the Manhattan distance of each sensor to its beacon
    # and eliminate those that are closer to a sensor than the beacon.
    spaces_to_check = list(overlapping_spaces)
    for space in spaces_to_check:
        for sensor in relevant_sensors:
            beacon_distance = abs(sensor["b_x"] - sensor["s_x"]) + abs(sensor["b_y"] - sensor["s_y"])
            space_distance = abs(space[0] - sensor["s_x"]) + abs(space[1] - sensor["s_y"])
            if space_distance < beacon_distance:
                overlapping_spaces.discard(space)
                break
    
    last_space =list(overlapping_spaces)[0]
    return last_space[0] * 4000000 + last_space[1]
    # This would work, but it'll take around 90 days to run on my computer.

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