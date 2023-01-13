import pygame
from utils import load_image, terminate, load_level
from startscreen import start_screen
from board import Board
import constants

FPS = 60
SIZE = WIDTH, HEIGHT = 1360, 720
TILE_WIDTH = TILE_HEIGHT = 50
BACKGROUND_COLOR = (0, 0, 0)
SPEED = 10
is_winter = True

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('BattleFront')
clock = pygame.time.Clock()

images = {constants.GROUND[0]: load_image(constants.GROUND[1], is_winter=is_winter),
          constants.FOREST[0]: load_image(constants.FOREST[1], is_winter=is_winter),
          constants.SMALL_STONE[0]: load_image(constants.SMALL_STONE[1], is_winter=is_winter),
          constants.STONE[0]: load_image(constants.STONE[1], is_winter=is_winter),
          constants.BUILDING_01[0]: load_image(constants.BUILDING_01[1], is_winter=is_winter),
          constants.BUILDING_02[0]: load_image(constants.BUILDING_02[1], is_winter=is_winter),
          constants.FALLEN_TREE[0]: load_image(constants.FALLEN_TREE[1], is_winter=is_winter),
          constants.FLAG[0]: load_image(constants.FLAG[1], is_winter=is_winter),

          constants.ANTI_TANKS_INFANTRY_1[0]: load_image(constants.ANTI_TANKS_INFANTRY_1[1]),
          constants.ANTI_TANKS_INFANTRY_2[0]: load_image(constants.ANTI_TANKS_INFANTRY_2[1]),
          constants.INFANTRY_1[0]: load_image(constants.INFANTRY_1[1]),
          constants.INFANTRY_2[0]: load_image(constants.INFANTRY_2[1]),
          constants.SUPPORT_TRUCK_1[0]: load_image(constants.SUPPORT_TRUCK_1[1]),
          constants.SUPPORT_TRUCK_2[0]: load_image(constants.SUPPORT_TRUCK_2[1]),
          constants.TANK_1[0]: load_image(constants.TANK_1[1]),
          constants.TANK_2[0]: load_image(constants.TANK_2[1]),
          constants.CAMERA_POINT[0]: load_image(constants.CAMERA_POINT[1]),
          }

HEX_SIZE = 26


class Camera:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)
        self.observers = []

    def add_observers(self, ob):
        self.observers.extend(ob)

    def move(self, vector):
        self.rect.move_ip(vector)

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, *group):
        super().__init__(*group)
        self.image = images.get(image)
        self.rect = self.image.get_rect()

    def draw(self):
        self.rect.move_ip(self.rect[0] - camera.rect[0], self.rect[1] - camera.rect[1])


def main():
    global camera

    min_camera_pos = [-TILE_WIDTH, -TILE_HEIGHT]
    max_camera_pos = [TILE_WIDTH * WIDTH, TILE_HEIGHT * HEIGHT]

    filename = "level_01.txt"
    map = load_level(filename)
    camera = Camera(-100, -100)
    board = Board(len(map[0]), len(map), HEX_SIZE)

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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            camera.move([0, SPEED])
            board.set_y_offset(camera.y)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            camera.move([0, -SPEED])
            board.set_y_offset(camera.y)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            camera.move([SPEED, 0])
            board.set_x_offset(camera.x)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            camera.move([-SPEED, 0])
            board.set_x_offset(camera.x)
        screen.fill(BACKGROUND_COLOR)

        board.draw_sprites(screen)
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


if __name__ == '__main__':
    main()
