import pygame
import random

class Pipe:
    def __init__(self, width, height):
        self.x = width
        self.width = 60
        self.gap = 300   # increased gap (easier)
        self.height = height
        self.gap_y = random.randint(150, 450)
        self.passed = False

    def update(self):
        self.x -= 1   # slower movement

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 200, 0), (self.x, 0, self.width, self.gap_y - self.gap // 2))
        pygame.draw.rect(screen, (0, 200, 0), (self.x, self.gap_y + self.gap // 2, self.width, self.height))

    def collide(self, bird):
        bird_left = bird.x
        bird_right = bird.x + 30   # bird width
        bird_top = bird.y
        bird_bottom = bird.y + 30  # bird height

        pipe_left = self.x
        pipe_right = self.x + self.width
        

        # Check horizontal overlap
        if bird_right > pipe_left and bird_left < pipe_right:
            
            gap_top = self.gap_y - self.gap // 2
            gap_bottom = self.gap_y + self.gap // 2

            # If bird is NOT inside gap → collision
            if bird_top < gap_top or bird_bottom > gap_bottom:
                return True

        return False