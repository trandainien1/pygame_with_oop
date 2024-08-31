import sys
import pygame
from pygame.image import load
from pygame.transform import scale_by

pygame.init()

# Global variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy bird')
clock = pygame.time.Clock()
background_surf = load('assets/background-night.png')
background_surf = scale_by(background_surf, factor=2)
background_rect = background_surf.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background_surf, background_rect)

    pygame.display.update()
    clock.tick(60)