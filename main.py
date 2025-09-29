import sys
import pygame

from platforma import Platform
from dron import Drone

from algoritmi import newton, gradient_descent, random_search, bfgs

algorithms = {
    "newton": newton,
    "random_search": random_search,
    "gradient_descent": gradient_descent,
    "bfgs": bfgs,
    }

def run_game(selected_algorithm):
    WIDTH, HEIGHT = 500, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Drone')

    original_pozadina = pygame.image.load("D:\PMF\Dron\slike\pozadina.jpg")
    original_dron = pygame.image.load('D:\PMF\Dron\slike\dron.png')
    original_platforma = pygame.image.load('D:\PMF\Dron\slike\platform.PNG')

    POZADINA = pygame.transform.scale(original_pozadina, (WIDTH, HEIGHT))

    platform = Platform(original_platforma, screen_height=HEIGHT, screen_width=WIDTH)

    algorithm = algorithms.get(selected_algorithm)
    if algorithm is None:
        print("Algoritam ne postoji")
        return

    dron = Drone(original_dron, screen_width=WIDTH, screen_height=HEIGHT, algorithm=algorithm)

    clock = pygame.time.Clock()
    running = True

    game_over = False
    font = pygame.font.SysFont(None, 30)

    result_text = None

    landed_count = 0
    crashed_count = 0

    while running:
        s = clock.tick(60)

        screen.fill((0, 0, 0))
        screen.blit(POZADINA, (0, 0))

        if not game_over:
            platform.update()
            platform.draw(screen)

            dron.update(platform, s)
            dron.draw(screen)

            if dron.state == "sleteo" and not game_over:
                landed_count += 1
                game_over = True
                dist = abs(dron.drone.centerx - platform.get_center_x())
                result_text = f"Uspešno sleteo! Distanca: {dist:.1f}px"

            elif dron.state == "pao" and not game_over:
                crashed_count += 1
                game_over = True
                result_text = "Dron je pao!"

        else:
            result = font.render(result_text, True, (255, 255, 255))
            instructions = font.render("Pritisni R za restart, ESC za izlaz", True, (255, 255, 255))

            screen.blit(result, (50, HEIGHT // 2 - 30))
            screen.blit(instructions, (50, HEIGHT // 2 + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        platform = Platform(original_platforma, screen_height=HEIGHT, screen_width=WIDTH)
                        dron = Drone(original_dron, screen_width=WIDTH, screen_height=HEIGHT, algorithm=algorithm)
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

    print(f"Ukupno sletanja: {landed_count}")
    print(f"Ukupno padova: {crashed_count}")
    pygame.quit()
    sys.exit()