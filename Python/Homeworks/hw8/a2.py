# Do not import any modules. If you do, the tester may reject your submission.

# Constants for the contents of the maze.

# The visual representation of a wall.
WALL = '#'

# The visual representation of a hallway.
HALL = '.'

# The visual representation of a brussels sprout.
SPROUT = '@'

# Constants for the directions. Use these to make Rats move.

# The left direction.
LEFT = -1

# The right direction.
RIGHT = 1

# No change in direction.
NO_CHANGE = 0

# The up direction.
UP = -1

# The down direction.
DOWN = 1

# The letters for rat_1 and rat_2 in the maze.
RAT_1_CHAR = 'J'
RAT_2_CHAR = 'P'


class Rat:
    """ A rat caught in a maze. """
    def __init__(self, symbol, r, c):
       self.symbol = symbol
       self.location = (r, c)
       self.score = 0

    def set_location(self, r, c):
        self.location = r, c

    def eat_sprout(self):
        self.score += 1

    def __str__(self):
        return '{} at ({}, {}) ate {} sprouts'.format(self.symbol, self.location[0], self.location[1], self.score)

class Maze:
    """ A 2D maze. """
    def __init__(self, maze, rat_1, rat_2):
        self.level = maze
        self.rat_1 = rat_1
        self.rat_2 = rat_2

    def is_wall(self, r, c):
        return self.level[r][c] == '#'

    def get_character(self, x, y):
        return self.level[x][y]

    def move(self, rat, v, h):
        if is_wall([rat.location[0] + v][rat.location[1] + h]):
            return False
        elif self.level[rat.location[0] + v][rat.location[1] + h] == '@':
            rat.eat_sprout()
            self.level[rat.location[0]][rat.location[1]] = HALL
            rat.set_location(rat.location[0] + v, rat.location[1] + h)
            self.level[rat.location[0]][rat.location[1]] = rat.symbol

            
            



