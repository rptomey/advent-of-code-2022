elves = []
current_elf = 0

with open("aoc22_1_input.txt") as f:
    for line in f:
        if line != "\n":
            current_elf += int(line)
        else:
            elves.append(current_elf)
            current_elf = 0

# Get the last elf in there, too, since there's not a blank line at the end of the input...
elves.append(current_elf)

# Sort in descending order
elves.sort(reverse=True)

# Sum up the first 3 elves
print(sum(elves[0:3]))

