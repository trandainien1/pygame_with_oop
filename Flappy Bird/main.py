import random
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

class Bird():
    def __init__(self):
        self.surfs = [load('assets/yellowbird-downflap.png'), load('assets/yellowbird-midflap.png'), load('assets/yellowbird-upflap.png')]
        self.surf_index = 0
        for i in range(len(self.surfs)):
            self.surfs[i] = scale_by(self.surfs[i], factor=2)
        self.rect = self.surfs[self.surf_index].get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.velocity = 0
        self.jump_height = -8
        self.gravity = 0.3
    def update(self, key_pressed):
        if key_pressed[pygame.K_SPACE]:
            self.velocity = self.jump_height

        self.rect.y += self.velocity
        self.velocity += self.gravity

        self.surf_index += 1
        if self.surf_index >= 15:
            self.surf_index = 0

    def rotate(self, surf):
        return pygame.transform.rotozoom(surf, angle=-self.velocity * 2, scale=1)

    def draw(self, screen):
        screen.blit(self.rotate(self.surfs[self.surf_index//5]), self.rect)

class Pipe():
    def __init__(self):
        self.surf = scale_by(load('assets/pipe-green.png'), factor=2)
        self.flipped_surf = pygame.transform.flip(scale_by(load('assets/pipe-green.png'), factor=2), flip_y=True, flip_x=False)
        self.rects = []
        self.flipped_rects = []
        self.heights = [450, 400, 350]
        self.animation_speed = 3

    def create_pipe(self):
        height = random.choice(self.heights)
        rect = self.surf.get_rect()
        rect.x = SCREEN_WIDTH
        rect.y = height
        self.rects.append(rect)

        flipped_rect = self.flipped_surf.get_rect(bottomleft=(SCREEN_WIDTH, rect.top - 200))
        self.flipped_rects.append(flipped_rect)

    def update(self):
        for i in range(len(self.rects)):
            self.rects[i].x -= self.animation_speed
            self.flipped_rects[i].x -= self.animation_speed

    def draw(self, screen):
        for i in range(len(self.rects)):
            screen.blit(self.surf, self.rects[i])
            screen.blit(self.flipped_surf, self.flipped_rects[i])


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
bird = Bird()
pipe = Pipe()

# Events
SPAWN_PIPE_ENVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_PIPE_ENVENT, 2000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_PIPE_ENVENT:
            pipe.create_pipe()
    key_pressed = pygame.key.get_pressed()

    floor.update()
    bird.update(key_pressed)
    pipe.update()

    screen.blit(background_surf, background_rect)
    pipe.draw(screen)
    floor.draw(screen)
    bird.draw(screen)

    pygame.display.update()
    clock.tick(60)