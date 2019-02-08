import pygame
import sys


clock = pygame.time.Clock()
SIZE = WIDTH, HEIGHT = 1200, 720
screen = pygame.display.set_mode(SIZE)
colors = pygame.Color


all_sprites = pygame.sprite.Group()

FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


class Brick(pygame.sprite.Sprite):
    pass


class Platform(pygame.sprite.Sprite):
    pass


class Ball(pygame.sprite.Sprite):
    pass


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

    pygame.display.flip()