import os
import sys
import pygame


def load_image(name, colorkey=None, is_winter=None):
    if is_winter:
        _dir = 'winter'
    elif is_winter is None:
        _dir = 'units'
    else:
        _dir = 'summer'
    fullname = os.path.join('data', 'images', _dir, name)
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
    return list(map(lambda x: x.ljust(max_width, '0'), level_map))
