import numpy as np
import pygame
import pickle


pygame.init()

# Define board constants
DISPLAY_MULTI = 9  # Change this to scale the display size
DISPLAY_SIZE = 90
DISPLAY_WIDTH = DISPLAY_SIZE * DISPLAY_MULTI
DISPLAY_HEIGHT = DISPLAY_SIZE * DISPLAY_MULTI
SQUARE_SIZE = DISPLAY_WIDTH // 3
CELL_SIZE = SQUARE_SIZE // 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
GREEN = (25, 205, 25)
RED = (205, 25, 25)

# Misc declarations
FONT = pygame.font.Font(None, 12 * DISPLAY_MULTI)
DISPLAY_SURFACE = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))


class Board:
    def __init__(self, grid):
        self.solved = False
        self.grid = grid
        self.size = 9
        self.cells = np.empty((self.size, self.size), Cell)  # Make a matrix with size x size made of Cells
        self.color = LIGHT_GRAY
        for x in range(self.size):
            for y in range(self.size):
                self.cells[y][x] = Cell(y, x, self.grid)

    def drawBoard(self):
        DISPLAY_SURFACE.fill(WHITE)

        # Draws each cell
        for arr in self.cells:
            for cell in arr:
                cell.drawCell()
                cell.possible = self.isValid(cell)
                if self.isWinner():
                    cell.num_color = GREEN

        # Draws major black lines
        for x in range(0, DISPLAY_WIDTH, SQUARE_SIZE):  # Vertical lines
            pygame.draw.line(DISPLAY_SURFACE, BLACK, (x, 0), (x, DISPLAY_HEIGHT), 3)
        for y in range(0, DISPLAY_WIDTH, SQUARE_SIZE):  # horizontal lines
            pygame.draw.line(DISPLAY_SURFACE, BLACK, (0, y), (DISPLAY_WIDTH, y), 3)

        pygame.display.update()

    def isValid(self, cell):
        if cell.num == 0:
            return True

        for i in range(0, 9):  # Excluding self
            if i != cell.x and self.cells[cell.y][i].num == cell.num:
                return False
            if i != cell.y and self.cells[i][cell.x].num == cell.num:
                return False

        # Calculate what 3x3 square we are at
        x0 = (cell.x // 3) * 3
        y0 = (cell.y // 3) * 3

        # Check if number exists in square
        for i in range(0, 3):
            for j in range(0, 3):  # Needed to exclude self
                if self.cells[y0 + i][x0 + j].num == cell.num and (y0 + i != cell.y and x0 + j != cell.x):
                    return False
        return True

    def isWinner(self):
        for arr in self.cells:
            for cells in arr:
                if not cells.possible or not cells.num != 0:
                    return False
        return True



class Cell:

    def __init__(self, y, x, grid):
        self.y = y
        self.x = x
        self.num = grid[y][x]
        self.pos = (x * CELL_SIZE, y * CELL_SIZE)
        self.border_color = LIGHT_GRAY
        self.num_color = BLACK
        self.thickness = 2
        self.active = False
        self.possible = True
        self.static = False
        self.txt_surface = FONT.render(str(self.num), True, self.num_color)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], CELL_SIZE, CELL_SIZE)
        if self.num != 0:
            self.static = True

    def drawCell(self):
        self.txt_surface = FONT.render(str(self.num), True, self.num_color)
        pygame.draw.rect(DISPLAY_SURFACE, self.border_color, self.rect, self.thickness)
        if not self.possible:
            self.num_color = RED
        else:
            self.num_color = BLACK
        if self.num != 0:
            # DISPLAY_MULTI is added to cords to center the text as it scales
            DISPLAY_SURFACE.blit(self.txt_surface,
                                 (self.rect.x + (DISPLAY_MULTI * 3), self.rect.y + (DISPLAY_MULTI * 1.5)))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.static:
            # If the user clicked on the cell rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
                self.thickness = 4
            else:
                self.active = False
            # Change the current color of the cell.
            self.border_color = GREEN if self.active else LIGHT_GRAY
        if event.type == pygame.KEYDOWN:
            if self.active:
                # Change everything back after return was hit
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.border_color = LIGHT_GRAY
                    self.thickness = 2
                elif event.key == pygame.K_BACKSPACE:
                    self.num = 0
                else:
                    try:
                        self.num += int(event.unicode)
                        if self.num > 9:
                            self.num = 9
                    except ValueError:
                        print("Value input error, expecting int")
                        self.num = 0

                # Re-render the text.
                self.txt_surface = FONT.render(str(self.num), True, self.num_color)
