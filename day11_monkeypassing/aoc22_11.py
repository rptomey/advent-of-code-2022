import sys
import re
import copy
import math

def parse(file_name):
    """Parse input"""
    monkeys = {}

    # Each Monkey is several rows of information starting with "Monkey N"
    monkey_n = 0
    with open(file_name) as f:
        for line in f:
            if re.match(r"Monkey", line):
                monkey_n = int(re.search(r"[0-9]+", line).group(0))
                monkeys[monkey_n] = {
                    "number": monkey_n,
                    "items": [],
                    "op_type": "",
                    "op_num": 0,
                    "test_denom": 0,
                    "true_target": 0,
                    "false_target": 0,
                    "inspections": 0
                }
            elif re.search(r"items", line):
                items = re.findall(r"[0-9]+", line)
                monkeys[monkey_n]["items"] = [int(item) for item in items]
            elif re.search(r"Operation", line):
                new_calc = line.split("=")[1].strip()
                calc_parts = new_calc.split()
                if calc_parts[2] == "old":
                    monkeys[monkey_n]["op_type"] = "power"
                    monkeys[monkey_n]["op_num"] = 2
                else:
                    match calc_parts[1]:
                        case "*":
                            monkeys[monkey_n]["op_type"] = "multiply"
                        case "+":
                            monkeys[monkey_n]["op_type"] = "add"
                        case "-":
                            monkeys[monkey_n]["op_type"] = "subtract"
                    monkeys[monkey_n]["op_num"] = int(calc_parts[2])
            elif re.search(r"Test", line):
                monkeys[monkey_n]["test_denom"] = int(re.search(r"[0-9]+", line).group(0))
            elif re.search(r"true", line):
                monkeys[monkey_n]["true_target"] = int(re.search(r"[0-9]+", line).group(0))
            elif re.search(r"false", line):
                monkeys[monkey_n]["false_target"] = int(re.search(r"[0-9]+", line).group(0))

    return monkeys

def part1(data):
    """Solve part 1."""
    data = copy.deepcopy(data)
    for i in range(20):
        for num in data.keys():
            monkey = data[num]
            while len(monkey["items"]) > 0:
                # Pull the next item
                monkey["inspections"] += 1
                item = monkey["items"].pop(0)
                # Increase worry level
                match monkey["op_type"]:
                    case "power":
                        item = item ** monkey["op_num"]
                    case "multiply":
                        item = item * monkey["op_num"]
                    case "add":
                        item = item + monkey["op_num"]
                    case "subtract":
                        item = item - monkey["op_num"]
                # Decrease worry level
                item = item // 3
                # Pass to another monkey
                if item % monkey["test_denom"] == 0:
                    data[monkey["true_target"]]["items"].append(item)
                else:
                    data[monkey["false_target"]]["items"].append(item)

    monkey_inspections = []
    for num in data.keys():
        monkey_inspections.append(data[num]["inspections"])
    
    return math.prod(sorted(monkey_inspections, reverse=True)[0:2])

def part2(data):
    """Solve part 2."""
    data = copy.deepcopy(data)
    denoms = []
    for num in data.keys():
        denoms.append(data[num]["test_denom"])
    least_common_multiple = math.lcm(*denoms)
    for i in range(10000):
        for num in data.keys():
            monkey = data[num]
            while len(monkey["items"]) > 0:
                # Pull the next item
                monkey["inspections"] += 1
                item = monkey["items"].pop(0)
                # Increase worry level
                match monkey["op_type"]:
                    case "power":
                        item = item ** monkey["op_num"]
                    case "multiply":
                        item = item * monkey["op_num"]
                    case "add":
                        item = item + monkey["op_num"]
                    case "subtract":
                        item = item - monkey["op_num"]
                # Decrease worry level
                #if item > least_common_multiple:
                item = item % least_common_multiple
                # Pass to another monkey
                if item % monkey["test_denom"] == 0:
                    data[monkey["true_target"]]["items"].append(item)
                else:
                    data[monkey["false_target"]]["items"].append(item)

    monkey_inspections = []
    for num in data.keys():
        monkey_inspections.append(data[num]["inspections"])
    
    return math.prod(sorted(monkey_inspections, reverse=True)[0:2]) 

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