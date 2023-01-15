import os
import sys
import pygame
import constants


FIRST_PLAYER_SIGNS = 'ISNT'
SECOND_PLAYER_SIGNS = 'KPMG'


def load_image(name, colorkey=None, is_winter=None):
    if is_winter:
        _dir = 'winter'
    elif is_winter is None:
        _dir = 'units'
    else:
        _dir = 'summer'
    if name == "fon.jpg": # Исключение для фонов
        fullname = os.path.join('data', 'images', name)
    else:
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


def load_images(is_winter):
    images = {
        constants.GROUND[0]: load_image(constants.GROUND[1], is_winter=is_winter),
        constants.FOREST[0]: load_image(constants.FOREST[1], is_winter=is_winter),
        constants.SMALL_STONE[0]: load_image(constants.SMALL_STONE[1], is_winter=is_winter),
        constants.STONE[0]: load_image(constants.STONE[1], is_winter=is_winter),
        constants.BUILDING_01[0]: load_image(constants.BUILDING_01[1], is_winter=is_winter),
        constants.BUILDING_02[0]: load_image(constants.BUILDING_02[1], is_winter=is_winter),
        constants.FALLEN_TREE[0]: load_image(constants.FALLEN_TREE[1], is_winter=is_winter),
        constants.FLAG[0]: load_image(constants.FLAG[1], is_winter=is_winter)
    }
    return images


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = os.path.join('data', 'levels', filename)
    if not os.path.isfile(filename):
        print(f"Файл с картой уровня '{filename}' не найден")
        terminate()
    commands = []
    level_map = []
    with open(filename, 'r') as mapFile:
        is_commands = False
        for line in mapFile:
            line = line.rstrip()
            if line == '***':  # Означает завершение карты. На следующей строке пишутся команды
                is_commands = True
            elif is_commands:
                commands.append(line)
            else:
                level_map.append(line)
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '0'), level_map)), commands


def generate_level(board, level, images):
    from main import Tile
    from units import BaseUnit, Infantry, AntiTanksInfantry, Tank, SupportTruck
    units_1 = []
    units_2 = []
    for y in range(board.height):
        for x in range(board.width):
            if level[y][x] in FIRST_PLAYER_SIGNS:
                if level[y][x] == constants.INFANTRY_1:
                    un = Infantry(1, board.board[y][x], board, level[y][x])
                elif level[y][x] == constants.ANTI_TANKS_INFANTRY_1:
                    un = AntiTanksInfantry(1, board.board[y][x], board, level[y][x])
                elif level[y][x] == constants.TANK_1:
                    un = Tank(1, board.board[y][x], board, level[y][x])
                else:
                    un = SupportTruck(1, board.board[y][x], board, level[y][x])
                board.set_unit(x, y, un)
                units_1.append(un)

                board.set_image(x, y, Tile(constants.GROUND[0], images,
                                           board.tiles_group))
            elif level[y][x] in SECOND_PLAYER_SIGNS:
                if level[y][x] == constants.INFANTRY_2:
                    un = Infantry(2, board.board[y][x], board, level[y][x])
                elif level[y][x] == constants.ANTI_TANKS_INFANTRY_2:
                    un = AntiTanksInfantry(2, board.board[y][x], board, level[y][x])
                elif level[y][x] == constants.TANK_2:
                    un = Tank(2, board.board[y][x], board, level[y][x])
                else:
                    un = SupportTruck(2, board.board[y][x], board, level[y][x])
                board.set_unit(x, y, un)
                units_2.append(un)

                board.set_image(x, y, Tile(constants.GROUND[0], images,
                                           board.tiles_group))
            else:
                board.set_image(x, y, Tile(level[y][x], images, board.tiles_group))
    return units_1, units_2
