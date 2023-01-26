import pygame
from constants import *


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def getPos(self):
        return self.row, self.col

    def isClosed(self):
        return self.color == BLUE

    def isOpen(self):
        return self.color == PINK

    def isBarrier(self):
        return self.color == BLACK

    def isStart(self):
        return self.color == RED

    def isEnd(self):
        return self.color == GREEN

    def reset(self):
        self.color = WHITE

    def makeStart(self):
        self.color = RED

    def makeClosed(self):
        self.color = BLUE

    def makeOpen(self):
        self.color = PINK

    def makeBarrier(self):
        self.color = BLACK

    def makeEnd(self):
        self.color = GREEN

    def makePath(self):
        self.color = YELLOW

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def updateNeighbors(self, grid):
        self.neighbors = []
        # Moving DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].isBarrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].isBarrier():  # Moving UP
            self.neighbors.append(grid[self.row - 1][self.col])

        # Moving RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].isBarrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].isBarrier():  # Moving LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):  # comparing two spots
        return False


def makeGrid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def h(p1, p2):  # Heuristic Function
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstructPath(cameFrom, current, draw):
    while current in cameFrom:
        current = cameFrom[current]
        current.makePath()
        draw()
    current.makeStart()


def drawGrid(win, rows, width):    # Drawing grid lines
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    drawGrid(win, rows, width)
    pygame.display.update()


def getClickedPos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col
