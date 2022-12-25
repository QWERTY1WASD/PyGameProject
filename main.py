import pygame
from board import Board
from random import randint

EMPTY_CELL = 0
MINE_CELL = 10
CLOSED_CELL = -1

CELL_SIZE = 30
NROWS = NCOLS = 20
COUNT_MINES = 50
WIDTH = NCOLS * CELL_SIZE
HEIGHT = NROWS * CELL_SIZE
SIZE = WIDTH, HEIGHT
TEXT_SCALE = 1

BACKGROUND = pygame.Color('black')
COLOR_MINE = pygame.Color('red')
COLOR_TEXT = pygame.Color(100, 255, 100)


class Minesweeper(Board):
    def __init__(self, width, height, count_mines, **kwargs):
        super().__init__(width, height, **kwargs)
        self.board = [[CLOSED_CELL] * width for _ in range(height)]
        assert count_mines < width * height
        assert count_mines > 0
        self.count_mines = count_mines
        while count_mines:
            row = randint(0, height - 1)
            col = randint(0, width - 1)
            if self.board[row][col] == CLOSED_CELL:
                self.board[row][col] = MINE_CELL
                count_mines -= 1
        self.font = pygame.font.Font(None, int(round(CELL_SIZE * TEXT_SCALE)))

    def render(self, screen: pygame.Surface):
        cell = pygame.Rect(0, 0, self.cell_size, self.cell_size)
        for row in range(self.height):
            for col in range(self.width):
                new_cell = cell.move(
                    self.left + self.cell_size * col,
                    self.top + self.cell_size * row
                )
                if self.board[row][col] == MINE_CELL:
                    pygame.draw.rect(screen, COLOR_MINE, new_cell, 0)
                elif self.board[row][col] != CLOSED_CELL:
                    text = self.font.render(str(self.board[row][col]), True, COLOR_TEXT)
                    screen.blit(text, (new_cell.centerx - text.get_rect().centerx,
                                       new_cell.centery - text.get_rect().centery))
        super().render(screen)

    def cells(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.board[row][col]
        return EMPTY_CELL

    def count_mines_around(self, row, col):
        count = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i == row and j == col:
                    continue
                count += self.cells(i, j) == MINE_CELL
        return count

    def open_cell(self, row, col):
        if self.cells(row, col) == CLOSED_CELL:
            self.board[row][col] = self.count_mines_around(row, col)
            if self.board[row][col] == EMPTY_CELL:
                for i in range(row - 1, row + 2):
                    for j in range(col - 1, col + 2):
                        if i == row and j == col:
                            continue
                        self.open_cell(i, j)

    def on_click(self, cell_coords):
        col, row = cell_coords
        self.open_cell(row, col)


pygame.init()
board = Minesweeper(NROWS, NCOLS, COUNT_MINES, cell_size=CELL_SIZE, left=0, top=0)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Папа сапёра')
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event)
    screen.fill(BACKGROUND)
    board.render(screen)
    pygame.display.flip()
pygame.quit()
