import string

with open("input.txt", "r") as f:
	input = f.read()

def removeWhitespace(string):
    ns = ""
    for i in string:
            if not i.isspace():
                    ns += i
    return ns

def parseInstruction(instruction):
	if type(instruction) == list:
		result = []
		for i in instruction:
			result.append(i.strip("move ").replace("from ", "").replace("to ", "").split(" "))
		return result
	elif type(instruction) == str:
		return instruction.strip("move ").replace("from ", "").replace("to ", "").split(" ")

def doInstruction(instruction, part = 0):
	global topCrates
	global crates
	amount, from_, to = int(instruction[0]), int(instruction[1]) - 1, int(instruction[2]) - 1
	
	if topCrates[to] - amount < 0:
		for i in range(amount):
			crates = [[" " for i in range(len(crates[0]))]] + crates
		topCrates = getTopCrates(crates)

	if part == 0:
		for i in range(amount):
			crates[topCrates[to] - 1][to] = crates[topCrates[from_]][from_]
			crates[topCrates[from_]][from_] = " "
			topCrates = getTopCrates(crates)
	else:
		for i in list(reversed(range(amount))):
			crates[topCrates[to] - 1][to] = crates[topCrates[from_] + i][from_]
			crates[topCrates[from_] + i][from_] = " "
			topCrates = getTopCrates(crates)		
		

def parseCrates(crates):
	columnsStr = crates[-1]
	columns = int(removeWhitespace(columnsStr)[-1])
	crates.pop(-1)
	rows = len(crates)
	result = [[" " for i in range(columns)] for i in range(rows)]

	for row, layer in enumerate(crates):
		for column, char in enumerate(layer):
			if char in letters:
				column = int(columnsStr[column]) - 1 
				result[row][column] = char

	return result

def getTopCrates(crates, letters = False):
	highestPoints = {}
	for row, layer in enumerate(crates):
		for column, crate in enumerate(layer):
			if crate != " " and highestPoints.get(column, None) == None:
				if letters:
					highestPoints[column] = crate
				else:
					highestPoints[column] = row

	for row, layer in enumerate(crates):
		for column, crate in enumerate(layer):
			if highestPoints.get(column, None) == None:
				if letters:
					highestPoints[column] = None
				else:
					highestPoints[column] = len(crates)
	return highestPoints


letters = string.ascii_letters

crates = input.split("\n\n")[0].split("\n")
instructions = input.split("\n\n")[1].split("\n")

crates = parseCrates(crates)
topCrates = getTopCrates(crates)

for instruction in instructions:
	doInstruction(parseInstruction(instruction))

finalTop0 = getTopCrates(crates, True)
result0 = ""
for i in range(len(crates[0])):
	result0 += finalTop0[i]

crates = input.split("\n\n")[0].split("\n")
instructions = input.split("\n\n")[1].split("\n")

crates = parseCrates(crates)
topCrates = getTopCrates(crates)

for instruction in instructions:
	doInstruction(parseInstruction(instruction), part = 1)

finalTop1 = getTopCrates(crates, True)
result1 = ""
for i in range(len(crates[0])):
	result1 += finalTop1[i]


print(f"Answer 1: {result0}\nAnswer 2: {result1}")