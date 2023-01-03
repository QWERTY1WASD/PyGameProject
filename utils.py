import os
import sys
import pygame


BARRIER = '#'
GROUND = '0'
CAMERA_POINT = '@'
INFANTRY = 'I'
INFANTRY_ENEMY = 'K'
TANK = 'T'
TANK_ENEMY = 'G'


def load_image(name, colorkey=None):
    fullname = os.path.join('data', 'images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        terminate()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = os.path.join('data', 'levels', filename)
    if not os.path.isfile(filename):
        print(f"Файл с картой уровня '{filename}' не найден")
        terminate()
    with open(filename, 'r') as mapFile:
        level_map = [line.rstrip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, vars):
    from main import Tile, PivotPoint, Infantry
    h = len(level)
    w = len(level[0])
    new_player, x, y = None, None, None
    for y in range(h):
        for x in range(w):
            if level[y][x] == GROUND:
                Tile('ground', x, y, vars)
            elif level[y][x] == BARRIER:
                Tile('barrier', x, y, vars)
            elif level[y][x] == CAMERA_POINT:
                Tile('ground', x, y, vars)
                new_player = PivotPoint(x, y, vars)
            elif level[y][x] == INFANTRY:
                Tile('ground', x, y, vars)
                Infantry('infantry', x, y, vars)
            elif level[y][x] == INFANTRY_ENEMY:
                Tile('ground', x, y, vars)
                Infantry('infantry_enemy', x, y, vars)
            # elif level[y][x] == TANK:
            #    Tile('ground', x, y, vars)
            #    new_player = PivotPoint(x, y, vars)
    return new_player, w, h
