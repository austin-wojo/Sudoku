import board
import pygame
import sys
from pygame.locals import *
from os import path
import traceback
import pickle

pygame.init()

# Define FPS
FPS = 10
FPS_CLOCK = pygame.time.Clock()

# Misc declarations
SCORE_FONT = pygame.font.Font(None, 80)
DISPLAY_SURFACE = pygame.display.set_mode((board.DISPLAY_WIDTH, board.DISPLAY_HEIGHT))
pygame.display.set_caption("Sudoku by Austin")


class Saver:
    def __init__(self):
        self.grid = game.grid
        self.filename = 'savefile.dat'
        directory = path.dirname(__file__)
        self.filename = path.join(directory, self.filename)

    def save(self, game):
        with open(self.filename, 'wb') as file:
            for x in range(9):
                for y in range(9):
                    self.grid = game.cells[y][x].num
            pickle.dump(self, file)

    def load(self):
        try:
            with open(self.filename, 'rb') as file:
                self.grid = pickle.load(file).grid
                print(self.grid)
        except Exception:
            traceback.print_exc()
            return


def possible(cells, y, x, n):
    # Check for number exist in row or column
    for i in range(0, 9):
        if cells[y][i].num == n:
            return False
        if cells[i][x].num == n:
            return False

    # Calculate what 3x3 square we are at
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3

    # Check if number exists in square
    for i in range(0, 3):
        for j in range(0, 3):
            if cells[y0 + i][x0 + j].num == n:
                return False
    return True


def solve_GUI(cells):
    # Iterate every location on the grid
    for y in range(9):
        for x in range(9):
            if cells[y][x].num == 0:  # If location is open
                for n in range(1, 10):  # Check if 1-9 is possible in that location
                    if possible(cells, y, x, n):
                        cells[y][x].num = n
                        yield from solve_GUI(cells)
                        board.drawBoard()
                        cells[y][x].num = 0
                return
    yield


if __name__ == "__main__":
    game = board.Board([
        [2, 9, 0, 0, 0, 0, 0, 7, 0],
        [3, 0, 6, 0, 0, 8, 4, 0, 0],
        [8, 0, 0, 0, 4, 0, 0, 0, 2],
        [0, 2, 0, 0, 3, 1, 0, 0, 7],
        [0, 0, 0, 0, 8, 0, 0, 0, 0],
        [1, 0, 0, 9, 5, 0, 0, 6, 0],
        [7, 0, 0, 0, 9, 0, 0, 0, 1],
        [0, 0, 1, 2, 0, 0, 3, 0, 6],
        [0, 3, 0, 0, 0, 0, 0, 5, 9]])
    generator = solve_GUI(game.cells)
    saver = Saver()

    while True:
        for event in pygame.event.get():

            # Exit block
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Check for key push
            if event.type == pygame.KEYDOWN:
                # "s" pushed
                if event.key == pygame.K_s:
                    saver.save(game)

                if event.key == pygame.K_l:
                    game.grid = saver.grid
                    print(game.grid)

                # Space bar pushed
                if event.key == pygame.K_SPACE:
                    try:
                        next(generator)
                    except StopIteration:
                        generator = solve_GUI(game.cells)
                        print("All possible solutions found")

            # Check if a cell was clicked
            for arr in game.cells:
                for cell in arr:
                    cell.handleEvent(event)

        game.drawBoard()
        FPS_CLOCK.tick(FPS)


