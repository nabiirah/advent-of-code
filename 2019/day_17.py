"""Advent of code 2019 Day 17 - Set and Forget."""


from collections import defaultdict


class VacuumCameras:
    """Class for the ASCII - intcode controlled vacuum robot and cameras."""

    def __init__(self, code):
        """Initialises ASCII system code (dict) and an input list."""
        self.code = code
        self.inputs = []
        self.pointer = 0

    def run_intcode(self):
        """Run intcode program on code."""
        relative_base = 0
        while True:
            opcode = self.code[self.pointer]

            if 99 < opcode <= 22210:
                opcode, modes = parse_instruction(opcode)
            else:
                modes = [0, 0, 0]

            if opcode == 99:   # halt
                return

            if modes[0] == 0:
                param_1 = self.code[self.pointer + 1]
            elif modes[0] == 1:
                param_1 = self.pointer + 1
            else:
                param_1 = self.code[self.pointer + 1] + relative_base

            if modes[1] == 0:
                param_2 = self.code[self.pointer + 2]
            elif modes[1] == 1:
                param_2 = self.pointer + 2
            else:
                param_2 = self.code[self.pointer + 2] + relative_base

            if modes[2] == 0:
                param_3 = self.code[self.pointer + 3]
            else:
                param_3 = self.code[self.pointer + 3] + relative_base

            if opcode == 1:   # addition
                self.code[param_3] = self.code[param_1] + self.code[param_2]
                self.pointer += 4

            elif opcode == 2:   # multiplication
                self.code[param_3] = self.code[param_1] * self.code[param_2]
                self.pointer += 4

            elif opcode == 3:   # input
                if self.inputs:
                    self.code[param_1] = self.inputs.pop(0)
                    self.pointer += 2
                else:
                    yield "Waiting on input"

            elif opcode == 4:   # output
                self.pointer += 2
                output = self.code[param_1]
                yield output

            elif opcode == 5:   # jump-if-true
                if self.code[param_1] == 0:
                    self.pointer += 3
                else:
                    self.pointer = self.code[param_2]

            elif opcode == 6:   # jump-if-false
                if self.code[param_1] != 0:
                    self.pointer += 3
                else:
                    self.pointer = self.code[param_2]

            elif opcode == 7:   # less than
                if self.code[param_1] < self.code[param_2]:
                    self.code[param_3] = 1
                else:
                    self.code[param_3] = 0
                self.pointer += 4

            elif opcode == 8:   # equals
                if self.code[param_1] == self.code[param_2]:
                    self.code[param_3] = 1
                else:
                    self.code[param_3] = 0
                self.pointer += 4

            elif opcode == 9:   # adjust relative base
                relative_base += self.code[param_1]
                self.pointer += 2

            else:
                print("Invalid or incorrectly parsed instruction.")
                return


def parse_instruction(value):
    """Return opcode and mode parsed from instruction value."""
    str_value = str(value)
    opcode = int(str_value[-2:])
    modes = [int(x) for x in list(str_value)[:-2]]
    while len(modes) != 3:
        modes.insert(0, 0)
    return (opcode, list(reversed(modes)))


intcode_dict = defaultdict(int)
with open('inputs/day_17.txt') as f:
    i = 0
    for instruction in f.read().split(','):
        intcode_dict[i] = int(instruction)
        i += 1

aft = VacuumCameras(intcode_dict.copy())
aft_run = aft.run_intcode()
scaffolds = []
row = []
while True:
    try:
        value = chr(next(aft_run))
        if value == '\n':
            if row:
                scaffolds.append(row)
                row = []
        else:
            row.append(value)

    except StopIteration:
        break

intersections = []
for y in range(len(scaffolds)):
    for x in range(len(scaffolds[0])):
        adjacent_scaffold = 4
        if scaffolds[y][x] != '#':
            continue
        adjacent = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
        for coords in adjacent:
            try:
                if scaffolds[coords[1]][coords[0]] == '#':
                    adjacent_scaffold -= 1
                if not adjacent_scaffold:
                    intersections.append((x, y))
                    break
            except IndexError:
                pass

# Answer One
print("Alignment sum:", sum([a * b for a,b in intersections]))

# Print scaffolds and calculate route by hand
for row in scaffolds:
    print("".join(row))

main = "B,C,B,A,C,A,C,A,B,A\n"
a = "R,12,L,10,L,6,R,10\n"
b = "R,12,L,6,R,12\n"
c = "L,8,L,6,L,10\n"
camera = "n\n"

inputs = main + a + b + c + camera
changed_intcode = intcode_dict.copy()
changed_intcode[0] = 2
aft_2 = VacuumCameras(changed_intcode)
aft_2_run = aft_2.run_intcode()
while True:
    try:
        space_dust = next(aft_2_run)
        if space_dust == "Waiting on input":
            aft_2.inputs.append(ord(inputs[0]))
            inputs = inputs[1:]

    except StopIteration:
        break

# Answer Two
print("Amount of space dust collected:", space_dust)
