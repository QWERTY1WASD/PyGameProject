import pygame
from utils import load_image, terminate, load_level
from startscreen import start_screen
from camera import Camera
from units import BaseUnit
from board import Board

FPS = 60
SIZE = WIDTH, HEIGHT = 1360, 720
TILE_WIDTH = TILE_HEIGHT = 32
OFFSET_BOARD = 50
BACKGROUND_COLOR = (0, 0, 0)
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('BattleFront')
clock = pygame.time.Clock()

GROUND = '0'

tile_images = {
        GROUND: load_image('tile003.png')
        # 'empty': load_image('grass.png')
}

# HEX_COUNT_WIDTH = 10
# HEX_COUNT_HEIGHT = 5
HEX_SIZE = 17


class Tile(pygame.sprite.Sprite):
    GROUND = load_image("tile003.png")

    def __init__(self, image, *group):
        super().__init__(*group)
        if image == GROUND:
            self.image = Tile.GROUND
        self.rect = self.image.get_rect()


def main():
    # img = load_image('tile003.png')
    filename = "level_01.txt"
    map = load_level(filename)
    board = Board(len(map[0]), len(map), HEX_SIZE, offset=OFFSET_BOARD)
    for y in range(board.height):
        for x in range(board.width):
            board.set_image(x, y, Tile(map[y][x], board.tiles_group))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event)
        screen.fill(BACKGROUND_COLOR)
        board.draw_sprites(screen)
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


if __name__ == '__main__':
    main()
