import random
import sys

import pygame

class Player():
    def __init__(self):
        self.running = self.get_run_imgs(s=2, e=8, action='run')
        self.jumping = self.get_run_imgs(s=1, e=3, action='jump')
        self.surfs = self.get_run_imgs(s=2, e=8, action='run')
        self.surf_index = 0
        self.rect = self.surfs[self.surf_index].get_rect(bottomleft=(100, 610))
        self.gravity = 1
        self.jumping_height = 20
        self.y_velocity = self.jumping_height
        self.is_jumping = False

    def get_run_imgs(self, s, e, action):
        result = []
        for i in range(s, e):
            url = f'assets/dino/{action}{i}.png'
            surf = pygame.image.load(url)
            surf = pygame.transform.scale_by(surf, factor=4)
            result.append(surf)
        return result

    def update(self, key_pressed):
        if key_pressed[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.surfs = self.jumping
            self.surf_index = 0

        if self.is_jumping:
            self.rect.y -= self.y_velocity
            self.y_velocity -= self.gravity
            print(self.y_velocity, self.jumping_height)
            if self.y_velocity < -self.jumping_height:
                self.is_jumping = False
                self.y_velocity = self.jumping_height
                self.surfs = self.running

    def animate(self):
        self.surf_index += 1
        if self.surf_index >= len(self.surfs):
            self.surf_index = 0

    def draw(self, screen):
        if self.surf_index % 3 == 0:
            screen.blit(self.surfs[self.surf_index], (self.rect.x, self.rect.y + 6))
        else:
            screen.blit(self.surfs[self.surf_index], self.rect)

class Background():
    def __init__(self):
        self.surf = pygame.image.load('assets/Other/Track.png')
        self.surf2 = pygame.image.load('assets/Other/Track.png')
        self.rect = self.surf.get_rect(topleft=(0, 600))
        self.rect2 = self.surf2.get_rect(topleft=(self.rect.right - 10, 600))

    def update(self):
        self.rect.x -= 6
        self.rect2.x -= 6
        if self.rect.right <= 0:
            self.rect.left = self.rect2.right - 10
        if self.rect2.right <= 0:
            self.rect2.left = self.rect.right - 10

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        screen.blit(self.surf2, self.rect2)

class Cactus():
    def __init__(self):
        self.cactus = [pygame.image.load('assets/Cactus/SmallCactus3.png'), pygame.image.load('assets/Cactus/LargeCactus3.png')]
        self.cactus_index = 0
        self.rect = self.cactus[self.cactus_index].get_rect(bottomright=(SCREEN_WIDTH, 610))

    def update(self):
        self.rect.x -= 6

        if self.rect.x < 0:
            self.rect.left = SCREEN_WIDTH
            self.cactus_index = random.randint(0, 1)

    def draw(self, screen):
        if self.cactus_index == 0:
            screen.blit(self.cactus[self.cactus_index], self.rect)
        else:
            screen.blit(self.cactus[self.cactus_index], (self.rect.x, self.rect.y - 20))

    def reset_position(self):
        self.rect.left = SCREEN_WIDTH

# initialize
pygame.init()
pygame.display.set_caption('Dinosaur Game')

# Global variables
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
player = Player()
background = Background()
cactus = Cactus()
playing = True
# Tạo font chữ
font = pygame.font.Font(None, 40)
text_surf = font.render('Press s to start the game', False, 'Black')

# Events
RUNNING_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(RUNNING_EVENT, 100)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if playing:
            if event.type == RUNNING_EVENT:
                player.animate()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    cactus.reset_position()
                    playing = True


    if playing:
        key_pressed = pygame.key.get_pressed()

        background.update()
        player.update(key_pressed)
        cactus.update()

        if player.rect.colliderect(cactus):
            playing = False

    screen.fill('White')
    background.draw(screen)
    player.draw(screen)
    cactus.draw(screen)

    if not playing:
        screen.blit(text_surf, (SCREEN_WIDTH//2 - text_surf.get_width()//2, SCREEN_HEIGHT//2 - text_surf.get_height()//2))

    pygame.display.update()
    clock.tick(60)
