import pygame
import sys
import math

from main import run_game

pygame.init()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Izbor algoritma')

FONT = pygame.font.SysFont(None, 25)

POZADINA = pygame.image.load('slike/pozadina.jpg')
POZADINA = pygame.transform.scale(POZADINA, (WIDTH, HEIGHT))

DRON = pygame.image.load('slike/dron.png')
DRON = pygame.transform.scale(DRON, (80, 80))

buttons = {
    "Slučajno pretraživanje": pygame.Rect(150, 350, 200, 60),
    "Gradijentni spust": pygame.Rect(150, 430, 200, 60),
    "Njutnov metod": pygame.Rect(150, 510, 200, 60),
    "Kvazi-Njutn BFGS": pygame.Rect(150, 590, 200, 60),
}

algorihm_map = {
    "Slučajno pretraživanje": "random_search",
    "Gradijentni spust": "gradient_descent",
    "Njutnov metod": "newton",
    "Kvazi-Njutn BFGS": "bfgs"
}

def draw_buttons(mouse_position):
    for text, rect in buttons.items():
        color = (70, 120, 220) if rect.collidepoint(mouse_position) else (50, 100, 200)
        pygame.draw.rect(screen, color, rect, border_radius=10)
        text_surface = FONT.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)


def main_menu():
    clock = pygame.time.Clock()
    dron_x = WIDTH / 2 - 40
    dron_y = 250
    s = 0

    while True:
        clock.tick(60)
        mouse_position = pygame.mouse.get_pos()

        screen.blit(POZADINA, (0, 0))

        dron_offset = 15 * math.sin(s / 20)
        screen.blit(DRON, (dron_x, dron_y + dron_offset))
        s += 1

        draw_buttons(mouse_position)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for algorithm_name, rect in buttons.items():
                    if rect.collidepoint(mouse_position):
                        selected_algorithm = algorihm_map[algorithm_name]
                        run_game(selected_algorithm)
                        return


if __name__ == '__main__':
    main_menu()