import random

import pygame

class Platform:
    def __init__(self, image, screen_height, screen_width):
        self.width = 100
        self.height = 20

        self.x = random.randint(0, screen_width) - self.width // 2
        self.y = int(screen_height * 0.5)

        self.platform = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.transform.scale(image, (self.width, self.height))

        self.speed = 2
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.direction = 1

    def update(self):
        self.speed += random.uniform(-1.5, 1.5)
        max_speed = 4
        if self.speed > max_speed:
            self.speed = max_speed
        elif self.speed < -max_speed:
            self.speed = -max_speed

        self.platform.x += int(self.speed)

        if self.platform.right > self.screen_width:
            self.platform.right = self.screen_width
            self.speed = -self.speed

        if self.platform.left < 0:
            self.platform.left = 0
            self.speed = -self.speed

        center_x = self.platform.centerx
        center_y = self.platform.centery

        self.platform.width = int(self.width)
        self.height = int(self.height)
        self.platform.centerx = center_x
        self.platform.centery = center_y


    def draw(self, screen):
        screen.blit(self.image, self.platform)


    def get_center_x(self):
        return self.platform.centerx