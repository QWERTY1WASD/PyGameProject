import pygame
from board import Board
from utils import terminate
from camera import Camera

FPS = 60
CELL_SIZE = 50
SIZE = WIDTH, HEIGHT = 1280, 720
TEXT_SCALE = 1
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Battlefront')
clock = pygame.time.Clock()

BACKGROUND = pygame.Color('black')


class Field(Board):
    def __init__(self, width, height, **kwargs):
        super().__init__(width, height, **kwargs)
        self.board = [0 * width for _ in range(height)]
        self.font = pygame.font.Font(None, int(round(CELL_SIZE * TEXT_SCALE)))

    def on_click(self, cell_coords):
        print(cell_coords)


class Pivot_point(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, vars):
        super().__init__(vars['player_group'], vars['all_sprites'])
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x + (TILE_WIDTH - self.image.get_width()) // 2,
            TILE_HEIGHT * pos_y + (TILE_HEIGHT - self.image.get_height()) // 2
        )


def main():
    board = Field(30, 15, cell_size=CELL_SIZE, left=0, top=0)
    camera = Camera(WIDTH, HEIGHT)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event)
        screen.fill(BACKGROUND)
        board.render(screen)
        camera.update(player)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


if __name__ == '__main__':
    main()
