import pygame
from pygame.math import Vector2
import math


class Hexagon:
    HORIZONTAL_HEXAGON = True
    COLOR = pygame.Color("white")
    SELECTED_COLOR = (25, 0, 175)

    def __init__(self, center, size):
        self.center_x = center[0]
        self.center_y = center[1]
        self.size = size
        self.points = [self.hex_corner(i) for i in range(6)]
        self.height = size * 2
        self.width = math.sqrt(3)/2 * self.height
        self.x, self.y = None, None
        self.is_active = False
        self.is_selected = False
        self.container = None  # Содержание клетки: [None, "UNIT", ...] для удобства определения
        self.sprite = pygame.sprite.Sprite()

    def set_active(self, value=None):
        if value is not None:
            self.is_active = value
        else:
            self.is_active = not self.is_active

    def get_center(self):
        return self.center_x, self.center_y

    def set_table_coords(self, x, y):
        self.x, self.y = x, y

    def get_table_coords(self):
        return self.x, self.y

    def hex_corner(self, i, offset_x=0, offset_y=0):
        increase = 0 if self.HORIZONTAL_HEXAGON else 30
        angle_deg = 60 * i + increase
        angle_rad = math.pi / 180 * angle_deg
        return round(self.center_x + self.size * math.cos(angle_rad)) + offset_x, \
            round(self.center_y + self.size * math.sin(angle_rad)) + offset_y

    def render(self, screen, offset_x, offset_y):
        self.points = [self.hex_corner(i, offset_x=offset_x, offset_y=offset_y) for i in range(6)]
        self.sprite.rect = self.get_top_left_coord()

        color = self.COLOR
        border = 2
        if self.is_active:
            border = 0
            color = self.SELECTED_COLOR
        elif self.is_selected:
            border = 1
            color = self.SELECTED_COLOR
        pygame.draw.polygon(screen, color, self.points, border)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_top_left_coord(self):
        x = self.points[3][0] + 2
        y = self.points[4][1]
        return x, y


class Board:
    def __init__(self, width, height, cell_size, offset_x=0, offset_y=0):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.a, self.b = None, None
        self.tiles_group = pygame.sprite.Group()

        self.board = []
        for y in range(self.height):
            temp = []
            for x in range(self.width):
                increase = 0
                if x % 2 == 1:
                    increase = self.cell_size * math.sqrt(3) / 2
                hexagon = Hexagon((int(x * self.cell_size * 3 / 2 + self.offset_x),
                                   int(y * self.cell_size * math.sqrt(3) + increase + self.offset_y)),
                                  self.cell_size)
                hexagon.set_table_coords(x, y)
                temp.append(hexagon)
            self.board.append(temp)

    def set_x_offset(self, x):
        self.offset_x = x

    def set_y_offset(self, y):
        self.offset_y = y

    def draw_sprites(self, screen):
        self.tiles_group.draw(screen)

    def render(self, screen: pygame.Surface):
        for y in range(self.height):
            for x in range(self.width):
                self.board[y][x].render(screen, self.offset_x, self.offset_y)

    # def on_hover(self, mouse_pos):
    #     hex = self.get_hex(mouse_pos)
    #     if hex is not None:
    #         hex.is_selected = True

    def isPointInHex(self, pos, hex: Hexagon):
        x = abs(pos[0] - hex.get_center()[0])
        y = abs(pos[1] - hex.get_center()[1])
        z = self.cell_size

        py1 = z * 0.86602540378
        px2 = z * 0.2588190451
        py2 = z * 0.9659258262

        p_angle_01 = -x * (py1 - y) - x * y
        p_angle_20 = -y * (px2 - x) + x * (py2 - y)
        p_angle_03 = y * z
        p_angle_12 = -x * (py2 - y) - (px2 - x) * (py1 - y)
        p_angle_32 = (z - x) * (py2 - y) + y * (px2 - x)
        is_inside_1 = (p_angle_01 * p_angle_12 >= 0) and (p_angle_12 * p_angle_20 >= 0)
        is_inside_2 = (p_angle_03 * p_angle_32 >= 0) and (p_angle_32 * p_angle_20 >= 0)
        return is_inside_1 or is_inside_2

    def get_cell(self, mouse_pos):
        for y in range(self.height):
            for x in range(self.width):
                if self.isPointInHex(mouse_pos, self.board[y][x]):
                    return self.board[y][x].get_table_coords()

    def on_click(self, cell_coords, event):
        if cell_coords is None:
            return
        x, y = cell_coords
        if event.button == pygame.BUTTON_LEFT:
            self.a = self.board[y][x]
            self.a.set_active()
        elif event.button == pygame.BUTTON_RIGHT:
            self.b = self.board[y][x]
            self.b.set_active()
            self.b.set_active()
        if self.a is not None and self.b is not None:
            for h in self.board:
                self.activate_hexes(h, False)
            self.a.set_active()
            self.b.set_active()
            self.find_way(self.a, self.b)

    def get_click(self, mouse_event):
        cell = self.get_cell(mouse_event.pos)
        self.on_click(cell, mouse_event)

    def draw_line(self, screen, a, b):
        pygame.draw.line(screen, "white", (a.center_x, a.center_y),
                         (b.center_x, b.center_y), 5)

    def round_hex(self, x, y):
        rx = round(x)
        ry = round(y)
        rz = round(-x - y)  # z = -_x-_y
        x_diff = abs(x - rx)  # Ошибка округления _x
        y_diff = abs(y - ry)  # Ошибка округления _y
        z_diff = abs(-x - y - rz)  # Ошибка округления z
        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry - rz  # Приведение под равенство
        elif y_diff > z_diff:
            ry = -rx - rz  # Приведение под равенство
        return rx, ry

    def hex_distance(self, a, b):
        x_a, y_a = a.get_table_coords()
        x_b, y_b = b.get_table_coords()
        xd = abs(x_a - x_b)
        yd = abs((y_a + (x_a % 2) / 2) - (y_b + (x_b % 2) / 2))
        if xd >= yd * 2:
            result = xd
        else:
            result = xd + (yd - xd / 2)
        return int(result)

    def activate_hexes(self, hexes, value):
        [_hex.set_active(value=value) for _hex in hexes]

    def diap(self, a, n):
        max_it = sum([x * 6 for x in range(1, n + 1)])
        result = []
        for y in range(self.height):
            for x in range(self.width):
                if max_it < 0:
                    break
                if self.hex_distance(a, self.board[y][x]) <= n:
                    result.append(self.board[y][x])
                    max_it -= 1
        self.activate_hexes(result, True)
        return result

    def find_way(self, a, b):
        x_a, y_a = a.get_table_coords()
        x_b, y_b = b.get_table_coords()
        way = []
        distance = self.hex_distance(a, b)
        if distance == 0:
            way.append(self.board[y_a][x_b])
            return way
        for i in range(distance + 1):
            x, y = Vector2.lerp(Vector2(x_a, y_a), Vector2(x_b, y_b), i / distance)
            rx, ry = self.round_hex(x + 0.01, y + 0.01)
            if i != 0:
                if self.hex_distance(way[-1], self.board[ry][rx]) > 1:
                    ry += way[-1].get_table_coords()[1] - ry
            if self.board[ry][rx] in way:
                ry += (y_b - y_a) // abs(y_b - y_a)
            way.append(self.board[ry][rx])
        self.activate_hexes(way, value=True)
        return way

    def set_image(self, x, y, image):
        h = self.board[y][x]
        h.sprite = image
        h.sprite.rect = h.sprite.image.get_rect()
        h.sprite.rect.move_ip(h.get_top_left_coord())
        self.tiles_group.add(h.sprite)

    def move_board(self, x, y):
        self.offset_x += x
        self.offset_y += y
