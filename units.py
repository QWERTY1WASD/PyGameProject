import pygame.sprite


class BaseUnit:
    def __init__(self, team, hex, image, health, attack_radius, attack_damage, moves, board, dead=False):
        self.team = team  # Принадлежность к команде
        self.hex = hex
        self.sprite = image
        self.max_health = health
        self.health = health
        self.attack_radius = attack_radius
        self.attack_damage = attack_damage
        self.moves = moves
        self.board = board
        self.dead = dead  # Жива ли пешка
        self.hex.container = "UNIT"

    def move(self, b):
        if self.moves <= 0 or self.dead:
            return
        distance = self.board.hex_distance(self.hex, b)
        if distance > self.moves:
            return
        way = self.board.find_way(self.hex, b)
        self.hex.container = None
        self.hex = b
        self.hex.container = "UNIT"

    def check_attack(self):  # Возвращает список клекот, которые можно атаковать
        out = []
        if self.dead:
            return
        hexes = self.board.diap(self.hex, self.attack_radius)
        for i in hexes:
            if i.container == "UNIT":
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
