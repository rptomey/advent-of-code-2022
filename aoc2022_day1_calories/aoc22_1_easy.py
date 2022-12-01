most_calories = 0
current_elf = 0

with open("aoc22_1_input.txt") as f:
    for line in f:
        if line != "\n":
            current_elf += int(line)
        else:
            if current_elf > most_calories:
                most_calories = current_elf
            current_elf = 0

# Just in case it's the last elf...
if current_elf > most_calories:
    most_calories = current_elf

print(most_calories)

