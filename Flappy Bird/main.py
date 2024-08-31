import sys
import pygame
from pygame.image import load
from pygame.transform import scale_by

pygame.init()

class Floor():
    def __init__(self):
        self.surf = load('assets/floor.png')
        self.animation_speed = 3
        self.rects = []
        for i in range(3):
            if i > 0:
                padding += self.surf.get_width()
            else:
                padding = 0
            self.rects.append(self.surf.get_rect(bottomleft=(padding, SCREEN_HEIGHT+20)))
        print(self.rects)

    def update(self):
        for i in range(len(self.rects)):
            self.rects[i].x -= self.animation_speed
            if self.rects[i].right < 0:
                self.rects[i].x = SCREEN_WIDTH

    def draw(self, screen):
        for rect in self.rects:
            screen.blit(self.surf, rect)


# Global variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy bird')
clock = pygame.time.Clock()
background_surf = load('assets/background-night.png')
background_surf = scale_by(background_surf, factor=2)
background_rect = background_surf.get_rect()
floor = Floor()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    floor.update()

    screen.blit(background_surf, background_rect)
    floor.draw(screen)

    pygame.display.update()
    clock.tick(60)