"""https://adventofcode.com/2022/day/2"""
input_file: str = "input.txt"
plays: list[tuple] = []
with open(input_file, 'r', newline='') as input_:
    for play, line in enumerate(input_):
        plays.append((line.strip('\n').split(' ')))

rock_paper_scissors: dict[str, tuple[str, int]] = {
    'A': ("Rock", 1),
    'B': ("Paper", 2),
    'C': ("Scissors", 3),
}
rock_paper_scissors['X']: tuple[str, int] = rock_paper_scissors['A']
rock_paper_scissors['Y']: tuple[str, int] = rock_paper_scissors['B']
rock_paper_scissors['Z']: tuple[str, int] = rock_paper_scissors['C']

result: dict[str, str] = {
    0: "Loss",
    3: "Draw",
    6: "Win",
}

results: dict[str, dict[str, int]] = {
    'A': {
        'X': 3,
        'Y': 6,
        'Z': 0,
    },
    'B': {
        'X': 0,
        'Y': 3,
        'Z': 6,
    },
    'C': {
        'X': 6,
        'Y': 0,
        'Z': 3,
    },
}

score: int = 0

for play, (opponent, you) in enumerate(plays):
    score += results[opponent][you] + rock_paper_scissors[you][1]
    print(f"""Play {play}
Opponent plays: {rock_paper_scissors[opponent][0]}, \
You play: {rock_paper_scissors[you][0]}.
The result is a {result[results[opponent][you]]}, \
for {results[opponent][you]} points. \
Plus {rock_paper_scissors[you][1]} \
points for selecting {rock_paper_scissors[you][0]}.
New score: {score}
""")

print(f"Final score is {score}")

## https://adventofcode.com/2022/day/2#part2
input("Press ENTER key for part 2...")
score: int = 0
rock_paper_scissors['X']: tuple[str, int] = ("Loss", 0)
rock_paper_scissors['Y']: tuple[str, int] = ("Draw", 3)
rock_paper_scissors['Z']: tuple[str, int] = ("Win", 6)
results: dict[str, dict[str, int]] = {
    'A': {
        'X': rock_paper_scissors['C'],
        'Y': rock_paper_scissors['A'],
        'Z': rock_paper_scissors['B'],
    },
    'B': {
        'X': rock_paper_scissors['A'],
        'Y': rock_paper_scissors['B'],
        'Z': rock_paper_scissors['C'],
    },
    'C': {
        'X': rock_paper_scissors['B'],
        'Y': rock_paper_scissors['C'],
        'Z': rock_paper_scissors['A'],
    },
}
for play, (opponent, you) in enumerate(plays):
    score += results[opponent][you][1] + rock_paper_scissors[you][1]
    print(f"""Play {play}
Opponent plays: {rock_paper_scissors[opponent][0]}, \
You play: {results[opponent][you][0]}.
The result is a {rock_paper_scissors[you][0]}, \
for {rock_paper_scissors[you][1]} points. \
Plus {results[opponent][you][1]} \
points for selecting {results[opponent][you][0]}.
New score: {score}
""")
print(f"Final score is {score}")