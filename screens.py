import pygame

import constants
from utils import load_image, terminate
from constants import *


def get_click(self, mouse_pos):
    if self.rect.collidepoint(mouse_pos):
        return True
    return False


def start_screen(screen: pygame.Surface):
    BUTTON_SIZE = 250, 250
    OFFSET = 100

    w, h = screen.get_size()

    intro_text = [["BattleFront", "white"],  # Изменён режим подачи текста, 1)Текст 2)Его цвет
                  ["Добро пожаловать на фронт, товарищ!", "gray"],
                  ["Скоро начнётся твоя миссия"],
                  ["Уничтожь врага, сохрани свои войска", "red"]]

    fon = pygame.transform.scale(load_image(STARTMENU), screen.get_size())  # Константа
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 80
    for line in intro_text:
        if len(line) == 1:
            line.append("black")
        string_rendered = font.render(line[0], 1, line[1])
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = (screen.get_size()[0] - intro_rect.size[0]) // 2 + 30  # Выравнивание по центру экрана
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    btn_1_rect = pygame.Rect(w // 2 - BUTTON_SIZE[0] - OFFSET, h // 2 - 50, *BUTTON_SIZE)
    btn_2_rect = pygame.Rect(w // 2 + OFFSET, h // 2 - 50, *BUTTON_SIZE)
    pygame.draw.rect(screen, "gray", btn_1_rect)
    pygame.draw.rect(screen, "gray", btn_2_rect)

    text_1 = font.render('1', 1, 'black')  # Кнопки и текст к ним
    text_2 = font.render('2', 1, 'black')

    coords_1 = btn_1_rect.move(OFFSET * 1.15, OFFSET)
    coords_2 = btn_2_rect.move(OFFSET * 1.15, OFFSET)

    screen.blit(text_1, coords_1)
    screen.blit(text_2, coords_2)

    FPS = 60
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_1_rect.collidepoint(pygame.mouse.get_pos()):
                    return constants.lvl_1
                elif btn_2_rect.collidepoint(pygame.mouse.get_pos()):
                    return constants.lvl_2
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            terminate()
        pygame.display.flip()
        clock.tick(FPS)


def update_end_screen(screen, outro_text, text_cords):
    TEXT_SIZE = 293

    font = pygame.font.Font(None, 70)
    cords = 80
    if text_cords > cords:
        screen.fill("black")
        for line in outro_text:
            if len(line) == 1:
                line.append("black")
            string_rendered = font.render(line[0], 1, line[1])
            intro_rect = string_rendered.get_rect()
            text_cords += 10
            intro_rect.top = text_cords
            intro_rect.x = (screen.get_size()[0] - intro_rect.size[0]) // 2 + 30
            text_cords += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        text_cords -= TEXT_SIZE
    return text_cords


def end_screen(screen: pygame.Surface, winner, score):
    FPS = 60
    clock = pygame.time.Clock()
    text_cords = screen.get_size()[1]
    outro_text = [[f"Победитель: {winner}", "gold"],
                  ["Итоги битвы:", "gray"],
                  [f"Очков набрано: {score}", "white"],
                  ["Хоть битва и окончена...", "white"],
                  ["Война ещё продолжается...", "red"]]
    with open("statistic.txt", 'w', encoding='utf-8') as f:
        print('\n'.join([text[0] for text in outro_text]), file=f)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        text_cords = update_end_screen(screen, outro_text, text_cords)
        pygame.display.flip()
        clock.tick(FPS)
