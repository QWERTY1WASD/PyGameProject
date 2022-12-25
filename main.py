import pygame
from board import Board

CELL_SIZE = 50
# WIDTH = NCOLS * CELL_SIZE
# HEIGHT = NROWS * CELL_SIZE
SIZE = WIDTH, HEIGHT = 1280, 720
TEXT_SCALE = 1

BACKGROUND = pygame.Color('black')


class Field(Board):
    def __init__(self, width, height, **kwargs):
        super().__init__(width, height, **kwargs)
        self.board = [0 * width for _ in range(height)]
        self.font = pygame.font.Font(None, int(round(CELL_SIZE * TEXT_SCALE)))

    def on_click(self, cell_coords):
        print(cell_coords)


pygame.init()
board = Field(30, 15, cell_size=CELL_SIZE, left=0, top=0)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Battlefront')
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
