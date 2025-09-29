import pygame
import random

pygame.mixer.init()

sound_effect = pygame.mixer.Sound('D:\PMF\Dron\Zvukovi\letenje drona.mp3')

class Drone:
    def __init__(self, image, screen_width, screen_height, algorithm=None):
        self.width = 60
        self.height = 60

        self.x = random.randint(50, screen_width - 50)
        self.y = screen_height - self.height - 10

        self.drone = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.transform.scale(image, (self.width, self.height))

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.algorithm = algorithm
        self.state = "poleti"
        self.speed = 3
        self.positions = []
        self.wind = 0
        self.wind_timer = 0

        self.sound_playing = False


    def draw(self, screen):
        for position in self.positions:
            pygame.draw.circle(screen, (0, 100, 255), position, 2)

        screen.blit(self.image, self.drone)


    def update_wind(self, s):
        self.wind_timer += s
        if self.wind_timer >= 1000:
            self.wind = random.uniform(-1.5, 1.5)
            self.wind_timer = 0


    def check_landing(self, platform):
        vertical = abs(self.drone.bottom - platform.platform.top) < 3
        horizontal = (self.drone.right > platform.platform.left) and (self.drone.left < platform.platform.right)

        return vertical and horizontal


    def save_positions(self):
        self.positions.append(self.drone.center)
        if len(self.positions) > 300:
            self.positions.pop(0)


    def update(self, platform, s):
        self.update_wind(s)

        distance = self.speed * (s / 16)
        wind_effect = self.wind * (s / 16)

        if not self.sound_playing and self.state in ["poleti", "sleti"]:
            sound_effect.play(-1)
            sound_effect.set_volume(0.5)
            self.sound_playing = True

        if self.state == "poleti":
            self.drone.y -= distance
            self.drone.x += wind_effect

            if self.drone.top <= 100:
                self.state = "sleti"

            if self.drone.left < 0:
                self.drone.left = 0
            if self.drone.right > platform.screen_width:
                self.drone.right = platform.screen_width

        elif self.state == "sleti":
            if self.algorithm:
                platform_x = platform.get_center_x()
                x = self.drone.centerx

                step = self.algorithm.optimize(x, platform_x, self.wind)
                self.drone.centerx = max(0, min(self.screen_width, x + step))

                self.drone.y += distance * 0.2

                if self.check_landing(platform):
                    self.drone.bottom = platform.platform.top
                    self.state = "sleteo"
                    self.speed = 0

                    sound_effect.fadeout(500)
                    sound_effect.stop()

                elif self.drone.top > self.screen_height:
                    self.state = "pao"
                    self.speed = 0
                    sound_effect.fadeout(500)
                    self.sound_playing = False

            else:
                self.drone.y += distance

        elif self.state == "sleteo":
            self.drone.centerx = platform.get_center_x()
            self.drone.bottom = platform.platform.top

            if self.sound_playing:
                sound_effect.fadeout(500)
                self.sound_playing = False


        self.save_positions()

