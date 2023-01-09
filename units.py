import pygame.sprite


class BaseUnit:
    # def __init__(self, opponent, _x, _y, image, health, attack_radius, attack_damage, moves):
    #    self.opponent = opponent
    #    self._x, self._y = _x, _y
    #    self.image = image
    #    self.max_health = health
    #    self.health = health
    #    self.attack_radius = attack_radius
    #    self.attack_damage = attack_damage
    #    self.moves = moves

    def move(self):
        pass

    def attack(self, enemy):
        enemy.change_health(-self.attack_damage)

    def change_health(self, value):
        self.health += value
        if self.health <= 0:
            self.kill()

    def kill(self):
        pass
