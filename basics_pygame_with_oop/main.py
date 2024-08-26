import math
import random
import sys

import pygame

screen_height = 800
screen_width = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption('Dinosaur game')

class Player():
    def __init__(self, size, x, y, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.next_step = {'x': 0, 'y': 0}
        self.bullets = []
        self.missiles = []

    def update(self, key_pressed, mouse_pressed, obs):
            self.next_step = {'x': 0, 'y': 0}

            if key_pressed[pygame.K_UP]:
                self.next_step['x'] = 0
                self.next_step['y'] = -10
            if key_pressed[pygame.K_DOWN]:
                self.next_step['x'] = 0
                self.next_step['y'] = 10
            if key_pressed[pygame.K_LEFT]:
                self.next_step['x'] = -10
                self.next_step['y'] = 0
            if key_pressed[pygame.K_RIGHT]:
                self.next_step['x'] = 10
                self.next_step['y'] = 0
            if key_pressed[pygame.K_SPACE]:
                self.create_bullet()

            if mouse_pressed[0]: # left mouse clicked
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.create_missile(mouse_x, mouse_y)

            self.rect.x += self.next_step['x']
            self.rect.y += self.next_step['y']

            if self.check_collision(obs):
                self.rect.x -= self.next_step['x']
                self.rect.y -= self.next_step['y']

            for bullet in self.bullets:
                bullet.update()

            for missile in self.missiles:
                missile.update()

    def check_collision(self, obs):
        for ob in obs:
            if self.rect.colliderect(ob):
                return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        for bullet in self.bullets:
            bullet.draw(screen)

        for missile in self.missiles:
            missile.draw(screen)

    def create_bullet(self):
        bullet = Bullet(x=self.rect.centerx, y=self.rect.top - 10, size=10, direction='up', color='Yellow')
        self.bullets.append(bullet)

    def create_missile(self, mouse_x, mouse_y):
        missile = Missile(
            x=self.rect.centerx,
            y=self.rect.centery,
            width=10,
            height=10,
            target_x=mouse_x,
            target_y=mouse_y,
            speed=10,
            color='Blue'
        )
        self.missiles.append(missile)


class Bullet():
    def __init__(self, x, y, size, color, direction):
        self.rect = pygame.Rect(x-size//2, y, size, size) # đặt đạn ở vị trí chính giữa nhân vật
        self.color = color
        self.direction = direction
    def update(self):
        if self.direction == 'up':
            self.rect.y -= 10
        if self.direction == 'down':
            self.rect.y += 10
        if self.direction == 'left':
            self.rect.x -= 10
        if self.direction == 'right':
            self.rect.x += 10

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Missile():
    def __init__(self, x, y, width, height, color, target_x, target_y, speed):
        self.rect = pygame.Rect(x-width//2,y-height//2, width, height)
        self.color = color
        angle = math.atan2(target_y-y, target_x-x)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

    def update(self):
        self.rect.x = self.rect.x + int(self.dx)
        self.rect.y = self.rect.y + int(self.dy)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Obstacle():
    def __init__(self):
        random_length = random.randint(10, 100)
        random_width = random.randint(10, 100)
        x_random = random.randint(0, screen_width)
        y_random = random.randint(0, screen_height)
        self.rect = pygame.Rect(x_random, y_random, random_width, random_length)
        self.color = pygame.Color((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

player = Player(size=20, x=0, y=0, color='Red')

obs = []
for i in range(10):
    obs.append(Obstacle())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.update(pygame.key.get_pressed(), pygame.mouse.get_pressed(), obs)


    screen.fill('Black')
    player.draw(screen)
    for ob in obs:
        ob.draw(screen)
    pygame.display.update()
    clock.tick(60)