import pygame
from utils import load_image, terminate
from constants import *


def get_click(self, mouse_pos):
    if self.rect.collidepoint(mouse_pos):
        return True
    return False


def start_screen(screen: pygame.Surface):
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
    for i in range(2):  # Прямоугольники для кнопок
        start_btn = pygame.Rect(272, 400, 340, 100)
        btn_2 = pygame.Rect(272, 400, 340, 100)
        pygame.draw.rect(screen, "gray", (272, 400, 340, 100))
        pygame.draw.rect(screen, "gray", (272 * 3, 400, 340, 100))

    FPS = 60
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(pygame.mouse.get_pos()):
                    return True
                elif btn_2.collidepoint(pygame.mouse.get_pos()):
                    pass  # Без понятия, как у тебя включается второй уровень
        pygame.display.flip()
        clock.tick(FPS)


def update_end_screen(screen, winner, score, text_cords):
    TEXT_SIZE = 293
    outro_text = [[f"Победитель: {winner}", "gold"],
                  ["Итоги битвы:", "gray"],
                  [f"Очков набрано: {score}", "white"],
                  ["Хоть битва и окончена...", "white"],
                  ["Война ещё продолжается...", "red"]]

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


def end_screen(screen: pygame.Surface, winner, score):  # Полный аналог start_screen
    FPS = 60
    clock = pygame.time.Clock()
    text_cords = screen.get_size()[1]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        text_cords = update_end_screen(screen, winner, score, text_cords)
        pygame.display.flip()
        clock.tick(FPS)
