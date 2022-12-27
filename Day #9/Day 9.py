from numpy import sign
from typing import List, Tuple
from time import sleep
import os, getopt, sys

FILEPATH = "inputs/day9.txt"
MANUAL_STEP = False
P_1 = False
P_2 = True
VISUALIZE = False
VISUALIZE_REFRESH_RATE = 0.5

# Type alias for a formatted instruction
Instr = Tuple[int, int]

class Knot():
    def __init__(self, i) -> None:
        self.i = str(i)
        self.x = 0
        self.y = 0
        self.leader: Knot = None    # previous knot in rope
        self.follower: Knot = None    # next knot in rope
        self._positions: List[Instr] = []

    def move(self, inst: Instr):

        if self.leader == None:
            self.x += inst[0]
            self.y += inst[1]
        
        else:
            diff_x = self.leader.x - self.x
            diff_y = self.leader.y - self.y

            if abs(diff_x) > 1 or abs(diff_y) > 1:
                self.x += sign(diff_x)
                self.y += sign(diff_y)
            
        if self.follower:
            return self.follower.move(inst)
        else:
            self._positions.append((self.x, self.y))
            return self.get_positions()

    def get_positions(self) -> int:
        return len(set(self._positions))

    def get_sprite(self) -> str:
        if self.leader == None:
            return "H"
        elif self.follower == None:
            return "T"
        else:
            return self.i


class Rope():
    def __init__(self, q) -> None:
        self.knots: List[Knot] = []
        for i in range(q):
            self.knots.append(Knot(i))
        
        for i, knot in enumerate(self.knots):
            if i == 0:
                knot.leader = None
                knot.follower = self.knots[i + 1]
            elif i == len(self.knots) - 1:
                knot.leader = self.knots[i - 1]
                knot.follower = None
            else:
                knot.leader = self.knots[i - 1]
                knot.follower = self.knots[i + 1]

        self.head = self.knots[0]
        self.tail = self.knots[-1]

    def move(self, inst: Instr):
        return self.head.move(inst)


class Grid():
    def __init__(self, rope: Rope) -> None:
        self.width = 60
        self.height = 16
        self.origin_x = self.width // 2
        self.origin_y = self.height // 2
        self.rope: Rope = rope
        self.head: Knot = rope.head
        self.tail: Knot = rope.tail

        # instantiate a blank grid
        self.reset()


    def display(self) -> None:
        os.system("clear")
        reversed_points = self.points
        reversed_points.reverse()
        for line in reversed_points:
            print("".join(line))
        print("=" * (self.width + 1))
        print("Tail total unique positions: ", self.tail.get_positions())
        print("Current instruction: ", self.inst)
        for knot in self.rope.knots[:len(self.rope.knots)//2]:
            print(f"{knot.get_sprite()}: ({knot.x}, {knot.y})", end="     ")
        print()
        for knot in self.rope.knots[len(self.rope.knots)//2:]:
            print(f"{knot.get_sprite()}: ({knot.x}, {knot.y})", end="     ")
        print()


    def reset(self) -> None:
        """
            Resets the grid to blank dots.
        """
        self.points: list = []
        for i in range(self.height):
            self.points.append([])
            for n in range(self.width + 2):
                if n == self.width + 1:
                    self.points[i].append("\n")
                else:
                    self.points[i].append(".")
        
        self.points[self.origin_y][self.origin_x] = "s"


    def update(self, inst) -> None:
        """
            Displays the rope on the grid by changing the dots at
            specific indexes to different characters.
        """
        self.inst = inst
        self.reset()
        for knot in self.rope.knots:
            # normalize position to account for origin not being
            # at (0,0)
            new_x = knot.x + self.origin_x
            new_y = knot.y + self.origin_y

            # account for out-of-bounds coordinates
            if new_x > self.width - 1 or new_x < self.width + 1:
                new_x = new_x % self.width

            if new_y > self.height - 1 or new_y < self.height + 1:
                new_y = new_y % self.height

            self.points[new_y][new_x] = knot.get_sprite()


def process_instructions(input) -> List[Instr]:
    """
        Parses instructions as single-unit movements on an X,Y plane.
        E.g.: "R 3" becomes, "[(1,0), (1,0), (1,0)]".
    """
    parsed_ins = []
    for line in input:
        #ins = parse_line(line)
        dir, quant = line.split()
        match dir:
            case "R":
                delta = (1, 0)
            case "L":
                delta = (-1, 0)
            case "U":
                delta = (0, 1)
            case "D":
                delta = (0, -1)
        parsed_ins += [(delta)] * int(quant)
    return parsed_ins


def feed_rope(instrs: List[Instr], rope: Rope, visualize: bool = False) -> int:
    """
        Feeds instructions one at a time to a Rope instance,
        which moves its children (knots), and returns the unique
        positions recorded by its last child (tail).
    """
    if visualize:
        grid = Grid(rope)
        grid.update(None)
        grid.display()
        if MANUAL_STEP:
            input()
        else:
            sleep(VISUALIZE_REFRESH_RATE)  

    for i, inst in enumerate(instrs):
        rope.move(inst)
        if visualize:
            grid.update(inst)
            grid.display()
            if MANUAL_STEP:
                input()
            else:
                sleep(VISUALIZE_REFRESH_RATE)
    
    return rope.tail.get_positions()


def main():
    input = [line.strip() for line in open(FILEPATH)]
    insts = process_instructions(input)

    if (P_1):
        part_1_rope = Rope(2)
        print("Part one: ", feed_rope(insts, part_1_rope, VISUALIZE))
        if (P_2):
            input("Press any key to move to part 2.")
    
    if (P_2):
        part_2_rope = Rope(10)
        print("Part two: ", feed_rope(insts, part_2_rope, VISUALIZE))


if __name__ == "__main__":
    abort = False
    args_list = sys.argv[1:]
    options = "hp:vsd:"
    long_options = ["help", "part=", "visualize", "step", "delay="]
    try:
        args, vals = getopt.getopt(args_list, options, long_options)
        for a, c in args:

            if a in ("-h", "--help"):
                print(__doc__)
                abort = True
                break

            if a in ("-p", "--part"):
                if int(c) == 1:
                    P_1 = True
                    P_2 = False
                elif int(c) == 2:
                    P_1 = False
                    P_2 = True
                else:
                    continue
            
            if a in ("-v", "--visualize"):
                VISUALIZE = True

            if a in ("-s", "--step"):
                VISUALIZE = True
                MANUAL_STEP = True

            elif a in ("-d", "--delay"):
                MANUAL_STEP = False
                VISUALIZE = True
                VISUALIZE_REFRESH_RATE = float(c)
    except getopt.error as e:
        print(str(e))
    
    if not abort:
        main()