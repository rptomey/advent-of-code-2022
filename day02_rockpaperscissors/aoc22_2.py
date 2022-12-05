import sys

def scoring(matchup):
    match matchup:
        case ['rock', 'paper']:
            return (6 + 2)
        case ['rock', 'scissors']:
            return (0 + 3)
        case ['rock', 'rock']:
            return (3 + 1)
        case ['paper', 'paper']:
            return (3 + 2)
        case ['paper', 'scissors']:
            return (6 + 3)
        case ['paper', 'rock']:
            return (0 + 1)
        case ['scissors', 'paper']:
            return (0 + 2)
        case ['scissors', 'scissors']:
            return (3 + 3)
        case ['scissors', 'rock']:
            return (6 + 1)

def parse(file_name):
    """Parse input."""
    key = {
            "A": "rock",
            "B": "paper",
            "C": "scissors",
            "X": "rock",
            "Y": "paper",
            "Z": "scissors"
    }
    matchups = []

    with open(file_name) as f:
        for line in f:
            matchup = [key[line[0]], key[line[2]]]
            matchups.append(matchup)
            
    return matchups

def alternative_parsing(file_name):
    matchups = []
    elf_key = {
        "A": "rock",
        "B": "paper",
        "C": "scissors"
    }
    what_beats = {
        "rock": "paper",
        "paper": "scissors",
        "scissors": "rock"
    }
    what_loses_to = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }

    with open(file_name) as f:
        for line in f:
            elf_play = elf_key[line[0]]
            match line[2]:
                case "X":
                    # need to lose
                    matchup = [elf_play, what_loses_to[elf_play]]
                    matchups.append(matchup)
                case "Y":
                    # need to draw
                    matchup = [elf_play, elf_play]
                    matchups.append(matchup)
                case "Z":
                    # need to win
                    matchup = [elf_play, what_beats[elf_play]]
                    matchups.append(matchup)

    return matchups

def part1(data):
    """Solve part 1."""
    total_score = 0

    for matchup in data:
        total_score += scoring(matchup)

    return total_score

def part2(data):
    """Solve part 2."""
    total_score = 0

    for matchup in data:
        total_score += scoring(matchup)
    
    return total_score

def solve(puzzle_input1, puzzle_input2):
    """Solve the puzzle for the given input."""
    solution1 = part1(puzzle_input1)
    solution2 = part2(puzzle_input2)

    return solution1, solution2

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input1 = parse(path)
        puzzle_input2 = alternative_parsing(path)
        solutions = solve(puzzle_input1, puzzle_input2)
        print("\n".join(str(solution) for solution in solutions))