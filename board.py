import pygame


class Board:
    cell_color = pygame.Color('white')
    cell_border = 1

    def __init__(self, width, height, left=10, top=10, cell_size=30):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def set_view(self, left=10, top=10, cell_size=30):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen: pygame.Surface):
        cell = pygame.Rect(0, 0, self.cell_size, self.cell_size)
        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(screen, self.cell_color, cell.move(
                    self.left + self.cell_size * col,
                    self.top + self.cell_size * row
                ), self.cell_border)

    def get_cell(self, mouse_pos):
        col = (mouse_pos[0] - self.left) // self.cell_size
        row = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= col < self.width and 0 <= row < self.height:
            return col, row

    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_event):
        cell = self.get_cell(mouse_event.pos)
        self.on_click(cell)
