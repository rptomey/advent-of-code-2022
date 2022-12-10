import sys
import re

def tick(cpu):
    cpu["cycles"] += 1

def update_register(cpu, amount):
    cpu["register"] += amount
    cpu["register_history"].append(amount)

def check_for_sample_time(cpu, cycles):
    if cycles in [20, 60, 100, 140, 180, 220]:
        get_signal_strength(cpu)

def get_signal_strength(cpu):
    cycles = cpu["cycles"]
    register = cpu["register"]
    cpu["signal_strength_samples"].append(cycles * register)

def draw(crt, cpu):
    current_row = which_row(cpu)
    drawing_position = cpu["cycles"] - (cpu["cycles"] // 40 * 40)
    if drawing_position == 0:
        drawing_position = 40
    drawing_position -= 1
    register = cpu["register"]
    sprite_range = [register-1,register, register+1]
    if drawing_position in sprite_range:
        crt[current_row].append("#")
    else:
        crt[current_row].append(" ")

def which_row(cpu):
    cycle = cpu["cycles"]
    if cycle <= 40:
        return 0
    elif 40 < cycle <= 80:
        return 1
    elif 80 < cycle <= 120:
        return 2
    elif 120 < cycle <= 160:
        return 3
    elif 160 < cycle <= 200:
        return 4
    elif 200 < cycle <= 240:
        return 5


def parse(file_name):
    """Parse input"""
    instructions = []

    # Each row is like "U 23", which would mean "go up 23 positions".
    with open(file_name) as f:
        for line in f:
            instruction = line.strip()
            instructions.append(instruction)

    return instructions

def handle_cpu_and_crt(data):
    """Solve both parts at the same time."""
    # Initialize the CPU, which tracks cycles, registers, and signal strength for part 1..
    cpu = {
        "cycles": 0,
        "register": 1,
        "register_history": [],
        "signal_strength_samples": []
    }

    # Initialize the CRT, which we'll draw on for part 2.
    crt = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: []
    }

    for instruction in data:
        if re.match(r"noop", instruction):
            tick(cpu)
            draw(crt, cpu)
            check_for_sample_time(cpu, cpu["cycles"])
        else:
            tick(cpu)
            draw(crt, cpu)
            check_for_sample_time(cpu, cpu["cycles"])
            pair = instruction.split()
            tick(cpu)
            draw(crt, cpu)
            check_for_sample_time(cpu, cpu["cycles"])
            update_register(cpu, int(pair[1]))
    
    for key in crt.keys():
        print("".join(crt[key]))

    return sum(cpu["signal_strength_samples"])

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    solution1 = handle_cpu_and_crt(puzzle_input)

    return solution1

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = parse(path)
        solutions = solve(puzzle_input)
        print(f"\n{solutions}")