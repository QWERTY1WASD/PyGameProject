import pygame
from utils import load_image, terminate, load_level
from startscreen import start_screen
from camera import Camera
from units import BaseUnit
from board import Board

FPS = 60
SIZE = WIDTH, HEIGHT = 1360, 720
TILE_WIDTH = TILE_HEIGHT = 32
OFFSET_BOARD = 100
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

HEX_COUNT_WIDTH = 10
HEX_COUNT_HEIGHT = 5
HEX_SIZE = 18.5


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        # if tile_type in obstacles:
        #     vars['obstacles_group'].add(self)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


tiles_group = pygame.sprite.Group()


def main():
    filename = "level_01.txt"
    map = load_level(filename)
    board = Board(HEX_COUNT_WIDTH, HEX_COUNT_HEIGHT, HEX_SIZE, offset=OFFSET_BOARD)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event)
        # keys = pygame.key.get_pressed()
        # old_player_rect = player.rect.copy()
        # if keys[pygame.K_UP] or keys[pygame.K_w]:
        #     player.rect.y -= TILE_WIDTH
        # if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        #     player.rect.y += TILE_WIDTH
        # if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        #     player.rect.x -= TILE_WIDTH
        # if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        #     player.rect.x += TILE_WIDTH
        # if pygame.sprite.spritecollideany(player, obstacles_group):
        #     player.rect = old_player_rect
        screen.fill(BACKGROUND_COLOR)
        tiles_group.draw(screen)
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


if __name__ == '__main__':
    main()
