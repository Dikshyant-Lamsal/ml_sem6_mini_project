import pygame
import os

class Bird:
    def __init__(self):
        self.x = 50
        self.y = 300
        self.vel = 0
        self.gravity = 0.3
        self.jump_strength = -6

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(BASE_DIR, "../assets/bird.png")

        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (30, 30))

    def update(self, action):
        if action == 1:
            self.vel = self.jump_strength

        self.vel += self.gravity
        self.y += self.vel

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))