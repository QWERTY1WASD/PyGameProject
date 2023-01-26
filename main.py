import pygame
import constants
from utils import terminate, load_level, generate_level, load_tiles
from screens import start_screen, end_screen
from board import Board
from ui import UI

FPS = constants.FPS
TILE_WIDTH = TILE_HEIGHT = constants.TILE_SIZE
BACKGROUND_COLOR = (0, 0, 0)
HEX_SIZE = constants.HEX_SIZE
UI_SIZE = UI_WIDTH, UI_HEIGHT = constants.UI_SIZE
EXIT_BUTTON_SIZE = constants.EXIT_BUTTON_SIZE

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
    elif len(units_2) == 0:
        end_screen(screen, 2, sum([u.get_points() for u in units_2]))
    if TURN % 2 == 0:
        [u.new_turn() for u in units_1]
    else:
        [u.new_turn() for u in units_2]


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, images, *group):
        super().__init__(*group)
        self.image = images.get(image)
        self.rect = self.image.get_rect()


def main():
    pygame.mixer.init()
    pygame.mixer.music.load(constants.SOVIET_MARCH)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    filename = start_screen(screen)

    first_player_group = pygame.sprite.Group()
    second_player_group = pygame.sprite.Group()

    map, commands = load_level(filename)
    is_winter = 'is_winter' in commands
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

    exit_btn_rect = pygame.Rect((screen.get_size()[0] - EXIT_BUTTON_SIZE[0], 0), EXIT_BUTTON_SIZE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_btn_rect.collidepoint(pygame.mouse.get_pos()):
                    end_screen(screen, "НИКТО", 0)
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
        ui.draw(screen, TURN)
        pygame.draw.rect(screen, "red", exit_btn_rect)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


if __name__ == '__main__':
    main()
