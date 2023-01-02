import pygame
from utils import load_image, terminate


def start_screen(screen: pygame.Surface):
    intro_text = ["BattleFront",
                  "Добро пожаловать на фронт, салага!",
                  "Правила игры",
                  "Уничтожь врага, сохрани свои войска"]

    fon = pygame.transform.scale(load_image('fon.jpg'), screen.get_size())
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 50
    for line in intro_text:
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
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)
