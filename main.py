import pygame
from utils import terminate, load_level, generate_level, load_tiles
from screens import start_screen, end_screen
from board import Board

FPS = 60
SIZE = WIDTH, HEIGHT = 1360, 720
TILE_WIDTH = TILE_HEIGHT = 50
BACKGROUND_COLOR = (0, 0, 0)
HEX_SIZE = 26
PLAYERS = [1, 2]

turn = 1  # Количество ходов

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('BattleFront')
clock = pygame.time.Clock()
score = [0, 0]  # Score system for 1 and 2 players


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, images, *group):
        super().__init__(*group)
        self.image = images.get(image)
        self.rect = self.image.get_rect()


def main():
    first_player_group = pygame.sprite.Group()
    second_player_group = pygame.sprite.Group()

    filename = "level_01.txt"
    map, commands = load_level(filename)
    is_winter = True if 'is_winter' in commands else False
    images = load_tiles(is_winter)
    current_pos = [0, 0]
    board = Board(len(map[0]), len(map), HEX_SIZE)
    board.set_x_offset(0)
    board.set_y_offset(0)

    current_player = 1
    start_screen(screen)  # Вызов стартового окна
    units_1, units_2 = generate_level(board, map, images)
    for u in units_1:
        first_player_group.add(u)
    for u in units_2:
        second_player_group.add(u)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event, current_player)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            current_pos[1] -= 1 if current_pos[1] != 0 else 0
            board.set_y_offset(-current_pos[1] * TILE_HEIGHT)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            current_pos[1] += 1 if current_pos[1] != len(map) // 3 else 0
            board.set_y_offset(-current_pos[1] * TILE_HEIGHT)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            current_pos[0] -= 1 if current_pos[0] != 0 else 0
            board.set_x_offset(-current_pos[0] * TILE_HEIGHT)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            current_pos[0] += 1 if current_pos[0] != len(map[0]) // 3 else 0
            board.set_x_offset(-current_pos[0] * TILE_HEIGHT)
        screen.fill(BACKGROUND_COLOR)

        board.draw_sprites(screen)
        board.render(screen)
        first_player_group.draw(screen)
        second_player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


if __name__ == '__main__':
    main()
