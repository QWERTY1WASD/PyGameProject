import pygame
import constants


class BaseUnit(pygame.sprite.Sprite):
    from utils import load_image
    units = {
        constants.INFANTRY_1[0]: load_image(constants.INFANTRY_1[1]),
        constants.INFANTRY_2[0]: load_image(constants.INFANTRY_2[1]),

        constants.ANTI_TANKS_INFANTRY_1[0]: load_image(constants.ANTI_TANKS_INFANTRY_1[1]),
        constants.ANTI_TANKS_INFANTRY_2[0]: load_image(constants.ANTI_TANKS_INFANTRY_2[1]),

        constants.TANK_1[0]: load_image(constants.TANK_1[1]),
        constants.TANK_2[0]: load_image(constants.TANK_2[1]),

        constants.SUPPORT_TRUCK_1[0]: load_image(constants.SUPPORT_TRUCK_1[1]),
        constants.SUPPORT_TRUCK_2[0]: load_image(constants.SUPPORT_TRUCK_2[1]),
    }

    def __init__(self, team, hex, board, image, health, attack_radius, attack_damage, moves):
        super().__init__()
        self.team = team  # Принадлежность к команде
        self.hex = hex

        self.image = BaseUnit.units.get(image)
        self.rect = self.image.get_rect()
        self.rect.move_ip(hex.get_top_left_coord())

        self.max_health = health
        self.health = health
        self.attack_radius = attack_radius
        self.attack_damage = attack_damage
        self.moves = moves
        self.board = board
        self.dead = False  # Жива ли пешка

    def move_diap(self):
        diap = self.board.diap(self.hex, self.moves)
        self.board.activate_hexes_moves(diap, True)

    def attack_diap(self):
        diap = self.board.diap(self.hex, self.moves)
        self.board.activate_hexes_attack(diap, True)

    def move(self, b):
        if self.moves <= 0 or self.dead:
            return
        distance = self.board.hex_distance(self.hex, b)
        if distance > self.moves:
            return
        way = self.board.find_way(self.hex, b)
        unit = self.hex.container
        self.hex.container = None
        self.hex = b
        self.hex.container = unit
        return way

    def check_attack(self):  # Возвращает список клеток, которые можно атаковать
        out = []
        if self.dead:
            return
        hexes = self.board.diap(self.hex, self.attack_radius)
        for i in hexes:
            if i.container is not None and i.container.team != self.team:
                out.append(i)
        return out

    def attack(self, enemy):
        if self.moves <= 0:
            return
        enemy.change_health(-self.attack_damage)

    def change_health(self, value):
        self.health += value
        if self.health <= 0:
            self.kill()

    def kill(self):  # Меняет значение self.dead на True, значение контейнера на None
        self.dead = True
        self.hex.container = None


class Infantry(BaseUnit):
    def __init__(self, team, hex, board, image, health=100, attack_radius=5,
                 attack_damage=25, moves=8):
        super().__init__(team, hex, board, image, health, attack_radius, attack_damage, moves)
        self.type = "INFANTRY"

    def attack(self, enemy):
        if self.moves <= 0:
            return
        baff = 1
        if enemy.type == "TANK":
            baff = 0.1
        enemy.change_health(-int(self.attack_damage * baff))


class AntiTanksInfantry(BaseUnit):
    def __init__(self, team, hex, board, image, health=50, attack_radius=7,
                 attack_damage=15, moves=6):
        super().__init__(team, hex, board, image, health, attack_radius, attack_damage, moves)
        self.type = "ANTI TANKS INFANTRY"

    def attack(self, enemy):
        if self.moves <= 0:
            return
        baff = 1
        if enemy.type == "TANK":
            baff = 3
        enemy.change_health(-int(self.attack_damage * baff))


class Tank(BaseUnit):
    def __init__(self, team, hex, board, image, health=250, attack_radius=6,
                 attack_damage=50, moves=12):
        super().__init__(team, hex, board, image, health, attack_radius, attack_damage, moves)
        self.type = "TANK"

    def attack(self, enemy):
        if self.moves <= 0:
            return
        baff = 1
        if "INFANTRY" in enemy.type:
            baff = 0.7
        enemy.change_health(-int(self.attack_damage * baff))


class SupportTruck(BaseUnit):
    def __init__(self, team, hex, board, image, health=100, attack_radius=0,
                 attack_damage=0, moves=15):
        super().__init__(team, hex, board, image, health, attack_radius, attack_damage, moves)
        self.type = "TANK"

    def attack(self, enemy):
        return
