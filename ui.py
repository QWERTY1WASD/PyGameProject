import pygame


class UI:
    COLOR_1_player = (210, 210, 210)
    COLOR_2_player = (235, 25, 25)
    COLOR = (35, 35, 35)
    OFFSET = 10

    def __init__(self, x, y, width, height, u_1, u_2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.units_1 = u_1
        self.units_2 = u_2

    def draw(self, screen, turn):
        width, height = screen.get_size()
        if turn % 2 == 0:
            color = self.COLOR_1_player
        else:
            color = self.COLOR_2_player
        pygame.draw.rect(screen, self.COLOR, self.rect, 0)
        points = [(width // 2 - self.OFFSET, self.height // 2 - self.OFFSET),
                  (width // 2 + self.OFFSET, self.height // 2),
                  (width // 2 - self.OFFSET, self.height // 2 + self.OFFSET)]
        pygame.draw.polygon(screen, color, points, 0)

    def set_units(self, u_1, u_2):
        self.units_1 = u_1
        self.units_2 = u_2

    def get_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def on_click(self, event):
        from main import change_turn
        mouse_pos = event.pos
        if self.get_click(mouse_pos) and event.button == pygame.BUTTON_LEFT:
            change_turn(self.units_1, self.units_2)
