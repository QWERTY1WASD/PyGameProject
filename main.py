import pygame

import constants
from utils import terminate, load_level, generate_level, load_tiles
from screens import start_screen, end_screen
from board import Board

FPS = constants.FPS
SIZE = WIDTH, HEIGHT = 1360, 720
TILE_WIDTH = TILE_HEIGHT = 50
BACKGROUND_COLOR = (0, 0, 0)
HEX_SIZE = 26
UI_SIZE = UI_WIDTH, UI_HEIGHT = 50, 50

turn = 0  # Количество ходов

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('BattleFront')
clock = pygame.time.Clock()
score = [0, 0]  # Score system for 1 and 2 players


def change_turn(units_1, units_2):
    global turn
    turn = (turn + 1) % 2
    if turn % 2 == 0:
        [u.new_turn() for u in units_1]
    else:
        [u.new_turn() for u in units_2]


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, images, *group):
        super().__init__(*group)
        self.image = images.get(image)
        self.rect = self.image.get_rect()


class UI:
    COLOR_1_player = (210, 210, 210)
    COLOR_2_player = (235, 25, 25)
    COLOR = (35, 35, 35)
    OFFSET = 10

    def __init__(self, x, y, width, height, u_1, u_2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.units_1 = u_1
        self.units_2 = u_2

    def draw(self, screen):
        if turn % 2 == 0:  # Если ходит первый игрок, то меняем цвет
            color = self.COLOR_1_player
        else:  # Иначе второй
            color = self.COLOR_2_player
        pygame.draw.rect(screen, self.COLOR, self.rect, 0)
        points = [(WIDTH // 2 - self.OFFSET, self.height // 2 - self.OFFSET),
                  (WIDTH // 2 + self.OFFSET, self.height // 2),
                  (WIDTH // 2 - self.OFFSET, self.height // 2 + self.OFFSET)]
        pygame.draw.polygon(screen, color, points, 0)

    def get_click(self, mouse_pos):  # Проверяет, было ли нажатие на rect
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def on_click(self, event):
        mouse_pos = event.pos
        if self.get_click(mouse_pos) and event.button == pygame.BUTTON_LEFT:
            change_turn(self.units_1, self.units_2)


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

    start_screen(screen)  # Вызов стартового окна
    units_1, units_2 = generate_level(board, map, images)

    ui = UI((WIDTH - UI_WIDTH) // 2, 0, UI_WIDTH, UI_HEIGHT, units_1, units_2)
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
                ui.on_click(event)
                board.get_click(event, turn)
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
        ui.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


if __name__ == '__main__':
    main()
