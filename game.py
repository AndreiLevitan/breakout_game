import pygame
import sys
import os


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color='blue-brick'):
        super().__init__(all_sprites)
        self.image = images[color]
        self.rect = self.image.get_rect().move(x, y)


class BrickPole:
    def __init__(self, lines, bricks):
        self.pole = []
        self.brick_width = WIDTH // bricks
        for i in range(lines):
            for j in range(bricks):
                x = j * self.brick_width
                y = j * 60
                self.place_brick(Brick(x, y, color='blue-brick'))

    def place_brick(self, brick):
        all_bricks.add(brick)
        print('Placed')


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)




clock = pygame.time.Clock()
SIZE = WIDTH, HEIGHT = 1200, 720
screen = pygame.display.set_mode(SIZE)
colors = pygame.Color


all_sprites = pygame.sprite.Group()
all_bricks = pygame.sprite.Group()

FPS = 50

images = {
    'blue-brick': load_image('images/bricks/blue_brick.png')
}

pole = BrickPole(3, 10)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

    all_sprites.draw(screen)
    all_bricks.draw(screen)
    pygame.display.flip()