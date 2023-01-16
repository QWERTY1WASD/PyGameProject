import pygame
import constants
from animation import AnimatedSprite


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
        self.can_attack = True

        self.max_moves = moves
        self.moves = moves
        self.board = board
        self.is_dead = False  # Жива ли пешка

    def display_move_and_attack(self):
        diap_move = self.board.diap(self.hex, self.moves)
        diap_attack = self.board.diap(self.hex, self.attack_radius)
        if self.moves > self.attack_radius:
            self.board.activate_hexes_moves(diap_move, True)
            # self.board.activate_hexes_moves(diap_attack, False)  # Не обязательно
            self.board.activate_hexes_attack(diap_attack, True)
        else:
            self.board.activate_hexes_attack(diap_attack, True)
            self.board.activate_hexes_attack(diap_move, False)
            self.board.activate_hexes_moves(diap_move, True)

    def move(self, b):
        if self.moves <= 0 or self.is_dead:
            return
        distance = self.board.hex_distance(self.hex, b)
        if distance > self.moves:
            return
        if b.container is not None:
            return
        way = self.board.find_way(self.hex, b)
        unit = self.hex.container
        self.moves -= distance
        self.hex.container = None
        self.hex = b
        self.hex.container = unit
        return way

    def check_attack(self):  # Возвращает список клеток, которые можно атаковать
        out = []
        hexes = self.board.diap(self.hex, self.attack_radius)
        for i in hexes:
            if i.container is not None and i.container.team != self.team:
                out.append(i.container)
        return out

    def attack(self, enemy):
        print(enemy)
        print(self.check_attack())
        print(enemy in self.check_attack())
        if not self.can_attack or enemy not in self.check_attack():
            return
        enemy.change_health(-self.attack_damage * self.get_baff(enemy))
        print(enemy.health)
        self.can_attack = False

    def new_turn(self):
        self.moves = self.max_moves
        self.can_attack = True

    def get_baff(self, enemy):
        baff = 1
        return baff

    def change_health(self, value):
        self.health += value
        if self.health <= 0:
            self.set_kill()

    def set_kill(self):  # Меняет значение self.is_dead на True, значение контейнера на None
        self.is_dead = True
        self.hex.container = None
        anim = AnimatedSprite(*self.hex.get_top_left_coord(), self)
        # super().kill()


class Infantry(BaseUnit):
    def __init__(self, team, hex, board, image, health=100, attack_radius=3,
                 attack_damage=25, moves=7):
        super().__init__(team, hex, board, image, health, attack_radius, attack_damage, moves)
        self.type = "INFANTRY"

    def get_baff(self, enemy):
        baff = 1
        if enemy.type == "TANK":
            baff = 0.1
        return baff


class AntiTanksInfantry(BaseUnit):
    def __init__(self, team, hex, board, image, health=50, attack_radius=7,
                 attack_damage=15, moves=8):
        super().__init__(team, hex, board, image, health, attack_radius, attack_damage, moves)
        self.type = "ANTI TANKS INFANTRY"

    def get_baff(self, enemy):
        baff = 1
        if enemy.type == "TANK":
            baff = 3
        return baff


class Tank(BaseUnit):
    def __init__(self, team, hex, board, image, health=250, attack_radius=6,
                 attack_damage=50, moves=10):
        super().__init__(team, hex, board, image, health, attack_radius, attack_damage, moves)
        self.type = "TANK"

    def get_baff(self, enemy):
        baff = 1
        if "INFANTRY" in enemy.type:
            baff = 0.7
        return baff


class SupportTruck(BaseUnit):
    def __init__(self, team, hex, board, image, health=100, attack_radius=0,
                 attack_damage=0, moves=12):
        super().__init__(team, hex, board, image, health, attack_radius, attack_damage, moves)
        self.type = "TANK"

    def attack(self, enemy):
        return
