import pygame
import sys
import os
import time


def update_screen():
    screen.fill(colors('black'))


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
        all_bricks.add(self)


class BrickPole:
    def __init__(self, lines, bricks):
        self.pole = []
        self.brick_width = WIDTH // (bricks + 0)
        self.margin = (WIDTH - self.brick_width * bricks) // 2
        for i in range(lines):
            for j in range(bricks):
                x = j * self.brick_width + self.margin
                y = i * 35
                self.place_brick(Brick(x, y, color='blue-brick'))

    def place_brick(self, brick):
        pass


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = images['platform']
        self.pos = (555, 650)
        self.rect = self.image.get_rect().move(self.pos)

    def move_platform(self, x):
        self.pos = x, self.pos[1]
        self.rect = self.image.get_rect().move(self.pos)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = images['ball']
        self.pos = (577, 600)
        self.rect = self.image.get_rect().move(self.pos)
        self.direction = (RIGHT, TOP)
        self.xv = 400
        self.yv = 400

    def check_collision(self):
        if pygame.sprite.spritecollideany(self, all_bricks):
            self.yv = -self.yv
        if self.pos[0] < 0:
            self.xv = abs(self.xv)
        if self.pos[0] > 1174:
            self.xv = -abs(self.xv)
        if self.pos[1] < 0:
            self.yv = -abs(self.yv)
        if self.pos[1] > 694:
            self.yv = abs(self.yv)
        if pygame.sprite.collide_rect(self, platform):
            self.yv = abs(self.yv)

    def move_circle(self, tick):
        xs = self.xv * tick / 1000
        ys = self.yv * tick / 1000
        self.pos = (
            self.pos[0] + self.direction[0] * xs,
            self.pos[1] + self.direction[1] * ys
        )

    def update(self, tick):
        self.check_collision()
        self.move_circle(tick)
        self.rect = self.image.get_rect().move(self.pos)



TOP = -1
DOWN = 1

RIGHT = 1
LEFT = -1


clock = pygame.time.Clock()
SIZE = WIDTH, HEIGHT = 1200, 720
screen = pygame.display.set_mode(SIZE)
colors = pygame.Color


all_sprites = pygame.sprite.Group()
all_bricks = pygame.sprite.Group()

FPS = 50

images = {
    'blue-brick': load_image('images/bricks/blue_brick.png'),
    'ball': load_image('images/ball.png'),
    'platform': load_image('images/platform.png')
}

pole = BrickPole(7, 12)
ball = Ball()
platform = Platform()


all_sprites.add(ball)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEMOTION:
            platform.move_platform(event.pos[0])

    all_sprites.draw(screen)
    tick = clock.tick()
    ball.update(tick)
    all_bricks.draw(screen)
    pygame.display.flip()
    update_screen()
