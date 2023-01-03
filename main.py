import pygame
from utils import load_image, terminate, generate_level, load_level
from startscreen import start_screen
from camera import Camera
from units import BaseUnit

FPS = 50
SIZE = WIDTH, HEIGHT = 1260, 720
TILE_WIDTH = TILE_HEIGHT = 50  # Todo: sprites size = 50 or 100
BACKGROUND_COLOR = (0, 0, 0)
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('BattleFront')
player = None
clock = pygame.time.Clock()


tile_images = {
    'ground': load_image('grass.png'),
    'barrier': load_image('barrier.png'),
    'infantry': load_image('infantry.png'),
    'infantry_enemy': load_image('infantry_enemy.png')
}
obstacles = {'barrier'}
player_image = load_image('point.png')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, vars):
        super().__init__(vars['tiles_group'], vars['all_sprites'])
        if tile_type in obstacles:
            vars['obstacles_group'].add(self)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class Infantry(BaseUnit, pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, vars):
        super().__init__(vars['tiles_group'], vars['all_sprites'])
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class PivotPoint(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, vars):
        super().__init__(vars['player_group'], vars['all_sprites'])
        self.image = player_image
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x + (TILE_WIDTH - self.image.get_width()) // 2,
            TILE_HEIGHT * pos_y + (TILE_HEIGHT - self.image.get_height()) // 2
        )


def main():
    global player, level_x, level_y, all_sprites, tiles_group, player_group, obstacles_group

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    obstacles_group = pygame.sprite.Group()
    start_screen(screen)
    # filename = input('Введите название уровня: ')
    filename = 'map.txt'
    player, level_x, level_y = generate_level(load_level(filename), globals())
    camera = Camera(WIDTH, HEIGHT)
    camera.add(player)
    camera.add_group(tiles_group)
    is_moving = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                is_moving = True
            elif event.type == pygame.KEYUP:
                is_moving = False
        if is_moving:
            old_player_rect = player.rect.copy()
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                player.rect.x -= TILE_WIDTH
            elif key[pygame.K_RIGHT]:
                player.rect.x += TILE_WIDTH
            elif key[pygame.K_UP]:
                player.rect.y -= TILE_HEIGHT
            elif key[pygame.K_DOWN]:
                player.rect.y += TILE_HEIGHT
            if pygame.sprite.spritecollideany(player, obstacles_group):
                player.rect = old_player_rect
        screen.fill(BACKGROUND_COLOR)
        # изменяем ракурс камеры
        camera.update(player)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


if __name__ == '__main__':
    main()
