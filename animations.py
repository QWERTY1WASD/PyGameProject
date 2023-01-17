import pygame
from utils import load_image
import constants


class AnimatedSprite(pygame.sprite.Sprite):
    SPRITE = load_image(constants.ANIM)
    COL = 5
    ROWS = 2
    FPS = 10

    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        self.cut_sheet(self.SPRITE, self.COL, self.ROWS)
        self.cur_frame = 0
        self.total_cur_frame = 0
        self.image = self.frames[0]
        self.rect = self.rect.move(x, y)
        self.fps = self.FPS

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
        if self.total_cur_frame >= (constants.FPS // self.fps):
            self.total_cur_frame = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if len(self.frames) - 1 == self.cur_frame:
            self.kill()
