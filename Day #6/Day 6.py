with open("input.txt", "r") as f:
	input = f.read()

def isUnique(string):
	ls = list(string); ls.sort()
	lss = list(set(string)); lss.sort()
	return ls == lss

def findUniqueSubstring(string, offset = 4):
	for i in range(len(string)):
		if isUnique(input[i:i + offset]):
			return i + offset

print(f"Answer 1: {findUniqueSubstring(input)}\nAnswer 2: {findUniqueSubstring(input, offset = 14)}")