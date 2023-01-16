import pygame
from utils import load_image, terminate
from constants import *


def start_screen(screen: pygame.Surface):
    intro_text = [["BattleFront", "orange"],  # Изменён режим подачи текста, 1)Текст 2)Его цвет
                  ["Добро пожаловать на фронт, салага!", "gray"],
                  ["Скоро начнётся твоя миссия", "gray"],
                  ["Уничтожь врага, сохрани свои войска", "red"]]

    fon = pygame.transform.scale(load_image(STARTMENU), screen.get_size())  # Константа
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 80
    for line in intro_text:
        if len(line) < 1:
            line.append("black")
        string_rendered = font.render(line[0], 1, line[1])
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = (screen.get_size()[0] - intro_rect.size[0]) // 2 + 30  # Выравнивание по центру экрана
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    for i in range(2):  # Прямоугольники для кнопок
        pygame.draw.rect(screen, "gray", (272, 400, 340, 100))
        pygame.draw.rect(screen, "gray", (272 * 3, 400, 340, 100))

    FPS = 60
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return True
        pygame.display.flip()
        clock.tick(FPS)


def end_screen(screen: pygame.Surface, score):  # Полный аналог start_screen
    outro_text = ["Итоги битвы:",
                  f"Очков набрано: {score}",
                  "Хоть битва и окончена...",
                  "Война ещё продолжается..."]

    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 50
    for line in outro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    FPS = 60
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return True
        pygame.display.flip()
        clock.tick(FPS)
