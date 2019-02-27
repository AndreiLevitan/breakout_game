import pygame
import sys
import os


def update_screen():
    screen.fill(colors('black'))
    bg.update()
    bg.draw()


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
        self.color = color
        self.image = images[self.color]
        self.rect = self.image.get_rect().move(x, y)
        all_bricks.add(self)

    def update(self, *args):
        if pygame.sprite.collide_rect(self, ball):
            self.damage()

    def delete(self):
        self.kill()

    def damage(self):
        if '-damaged' not in self.color:

            self.color += '-damaged'
            self.image = images[self.color]
        else:
            self.delete()


class BrickPole:
    def __init__(self, lines, bricks):
        self.pole = []
        self.brick_width = WIDTH // (bricks + 0)
        self.margin = (WIDTH - self.brick_width * bricks) // 2
        for layer in range(lines):
            for j in range(bricks):
                x = j * self.brick_width + self.margin
                y = layer * 35
                if layer in [1, 0]:
                    brick = 'red-brick'
                else:
                    brick = 'blue-brick'
                self.place_brick(Brick(x, y, color=brick))

    def place_brick(self, brick):
        self.pole.append(brick)

    def check_collision(self):
        all_bricks.update()


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = images['platform']
        self.pos = (555, 650)
        self.rect = self.image.get_rect().move(self.pos)

    def move_platform(self, x):
        self.pos = x, self.pos[1]
        self.rect = self.image.get_rect().move(self.pos)


class Trail(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = images['ball-hot']
        self.pos = pos
        self.rect = self.image.get_rect().move(self.pos)

    def draw(self):
        screen.blit(self.image, self.rect)


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = [0, 0]
        self.image = images['background']
        self.rect = self.image.get_rect().move(self.pos)
        self.xv = 5
        self.dir = LEFT

    def update(self):
        xs = self.xv * tick / 1000
        if self.pos[0] > 0:
            self.dir = LEFT
        if self.pos[0] < -720:
            self.dir = RIGHT
        self.pos[0] += xs * self.dir
        self.rect = self.image.get_rect().move(self.pos)

    def draw(self):
        screen.blit(self.image, self.rect)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = images['ball']
        self.pos = (577, 600)
        self.rect = self.image.get_rect().move(self.pos)
        self.trail = []
        self.direction = [RIGHT, TOP]
        self.xv = 500
        self.yv = 500

    def check_collision(self):
        if pygame.sprite.spritecollideany(self, all_bricks):
            self.direction[1] = -self.direction[1]
            self.xv += 6
            self.yv += 6
            pole.check_collision()
        if self.pos[0] < 0:
            self.direction[0] = RIGHT
        if self.pos[0] > 1174:
            self.direction[0] = LEFT
        if self.pos[1] < 0:
            self.direction[1] = DOWN
        if self.pos[1] > 694:
            self.direction[1] = TOP
        if pygame.sprite.collide_rect(self, platform):
            self.direction[1] = TOP

    def move_circle(self, tick):
        xs = self.xv * tick / 1000
        ys = self.yv * tick / 1000
        self.pos = (
            self.pos[0] + self.direction[0] * xs,
            self.pos[1] + self.direction[1] * ys
        )

    def update(self, tick):
        self.check_collision()
        self.trail.append(Trail(self.pos))
        self.trail = self.trail[-3:]
        for trail in self.trail:
            trail.update()
            trail.draw()

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

FPS = 120

images = {
    'blue-brick': load_image('images/bricks/blue_brick.png'),
    'blue-brick-damaged': load_image('images/bricks/blue_brick_damaged.png'),
    'red-brick': load_image('images/bricks/red_brick.png'),
    'red-brick-damaged': load_image('images/bricks/red_brick_damaged.png'),
    'ball': load_image('images/ball.png'),
    'ball-hot': load_image('images/ball_hot.png'),
    'platform': load_image('images/platform.png'),
    'background': load_image('images/bg.png')
}

pole = BrickPole(7, 12)
ball = Ball()
platform = Platform()
bg = Background()


all_sprites.add(ball)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEMOTION:
            platform.move_platform(event.pos[0])


    tick = clock.tick()
    ball.update(tick)
    all_bricks.draw(screen)
    all_sprites.draw(screen)
    pygame.display.flip()
    update_screen()
