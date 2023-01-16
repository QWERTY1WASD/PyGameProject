import constants
import pygame
from utils import get_anim_sprite


class AnimatedSprite(pygame.sprite.Sprite):
    COLUMS = 5
    ROWS = 2

    def __init__(self, x, y, unit):
        super().__init__()
        self.sprite = get_anim_sprite("boom.png")
        self.frames = []
        self.cut_sheet(self.sprite, self.COLUMS, self.ROWS)
        self.cur_frame = 0
        self.total_cur_frame = 0
        self.image = self.frames[0]
        self.rect = self.rect.move(x, y)
        self.fps = constants.FPS
        self.unit = unit

    def set_fps(self, new_fps):
        self.fps = new_fps

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.total_cur_frame += 1
        if self.total_cur_frame >= (self.fps // self.fps):
            self.total_cur_frame = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if self.cur_frame == self.frames[-1]:
            self.unit.kill()
            self.kill()
