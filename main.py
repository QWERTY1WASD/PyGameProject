import pygame
import constants
from utils import terminate, load_level, generate_level, load_tiles
from screens import start_screen, end_screen
from board import Board

FPS = constants.FPS
TILE_WIDTH = TILE_HEIGHT = constants.TILE_SIZE
BACKGROUND_COLOR = (0, 0, 0)
HEX_SIZE = constants.HEX_SIZE
UI_SIZE = UI_WIDTH, UI_HEIGHT = constants.UI_SIZE

TURN = constants.TURN

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SIZE = WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption('BattleFront')
clock = pygame.time.Clock()
sound_boom = pygame.mixer.Sound(constants.BOOM)


def change_turn(units_1, units_2):
    global TURN
    TURN = (TURN + 1) % 2
    if len(units_1) == 0:
        end_screen(screen, 2, sum([u.get_points() for u in units_2]))
        terminate()
    elif len(units_2) == 0:
        end_screen(screen, 1, sum([u.get_points() for u in units_1]))
        terminate()
    if TURN % 2 == 0:
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
        if TURN % 2 == 0:  # Если ходит первый игрок, то меняем цвет
            color = self.COLOR_1_player
        else:  # Иначе второй
            color = self.COLOR_2_player
        pygame.draw.rect(screen, self.COLOR, self.rect, 0)
        points = [(WIDTH // 2 - self.OFFSET, self.height // 2 - self.OFFSET),
                  (WIDTH // 2 + self.OFFSET, self.height // 2),
                  (WIDTH // 2 - self.OFFSET, self.height // 2 + self.OFFSET)]
        pygame.draw.polygon(screen, color, points, 0)

    def set_units(self, u_1, u_2):
        self.units_1 = u_1
        self.units_2 = u_2

    def get_click(self, mouse_pos):  # Проверяет, было ли нажатие на rect
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def on_click(self, event):
        mouse_pos = event.pos
        if self.get_click(mouse_pos) and event.button == pygame.BUTTON_LEFT:
            change_turn(self.units_1, self.units_2)


def main():
    pygame.mixer.init()
    pygame.mixer.music.load(constants.SOVIET_MARCH)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    filename = start_screen(screen)  # Вызов стартового окна

    first_player_group = pygame.sprite.Group()
    second_player_group = pygame.sprite.Group()

    map, commands = load_level(filename)
    is_winter = True if 'is_winter' in commands else False
    images = load_tiles(is_winter)
    current_pos = [0, 0]
    board = Board(len(map[0]), len(map), HEX_SIZE)
    board.set_x_offset(0)
    board.set_y_offset(0)

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
                ui.set_units(board.get_units(0), board.get_units(1))
                ui.on_click(event)
                board.get_click(event, TURN)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            current_pos[1] -= 1 if current_pos[1] != 0 else 0
            board.set_y_offset(-current_pos[1] * TILE_HEIGHT)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            current_pos[1] += 1 if current_pos[1] != len(map) - len(map) // 4 else 0
            board.set_y_offset(-current_pos[1] * TILE_HEIGHT)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            current_pos[0] -= 1 if current_pos[0] != 0 else 0
            board.set_x_offset(-current_pos[0] * TILE_HEIGHT)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            current_pos[0] += 1 if current_pos[0] != len(map[0]) - len(map[0]) // 4 else 0
            board.set_x_offset(-current_pos[0] * TILE_HEIGHT)

        screen.fill(BACKGROUND_COLOR)
        board.draw_sprites(screen)
        board.render(screen)
        first_player_group.draw(screen)
        second_player_group.draw(screen)
        board.draw_anim(screen)
        ui.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


if __name__ == '__main__':
    main()
