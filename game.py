import pygame
import sys
import os


# обновляет screen
def update_screen():
    screen.fill(colors('black'))
    bg.update()
    bg.draw()


# выходит из игры
def terminate():
    pygame.quit()
    sys.exit()


# загружает изображение
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


# загружает звук
def load_sound(name):
    path = os.path.join('data', name)
    
    try:
        sound = pygame.image.load(path)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    return pygame.mixer.Sound(sound)


# основной класс, отвечающий за кирчпич
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color='blue-brick'):
        super().__init__(all_sprites)
        self.color = color
        self.image = images[self.color]
        self.rect = self.image.get_rect().move(x, y)

        self.sound_delete = sounds['delete']
        self.sound_damage = sounds['damage']
        all_bricks.add(self)

    # проверяет коллизию
    def update(self, *args):
        if pygame.sprite.collide_rect(self, ball):
            self.damage()

    # удаляет кирпич
    def delete(self):
        indicator.add_combo()
        self.kill()

    # расчитывает попадание по кирпичу
    def damage(self):
        if '-damaged' not in self.color:
            self.sound_damage.play()
            self.sound_damage.set_volume(2.0)

            self.color += '-damaged'
            self.image = images[self.color]
        else:
            self.sound_delete.play()
            self.delete()


# основной класс, отвечающий за расположение кирпичей на поле
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

    # добавляет кирпич на поле
    def place_brick(self, brick):
        self.pole.append(brick)

    # проверяет коллизию
    def check_collision(self):
        all_bricks.update()


# основной класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = images['platform']
        self.pos = (555, 650)
        self.rect = self.image.get_rect().move(self.pos)

    # передвигает платформу на x
    def move_platform(self, x):
        self.pos = x, self.pos[1]
        self.rect = self.image.get_rect().move(self.pos)


# основной класс, отвечающий за след мяча
# оставляет в координате передвижение мяча его призрак,
# создавая "след"
class Trail(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = images['ball-hot']
        self.pos = pos
        self.rect = self.image.get_rect().move(self.pos)

    def draw(self):
        screen.blit(self.image, self.rect)


# класс, отвечающий за задний фон
# плавно его передвигает
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = [0, 0]
        self.image = images['background']
        self.rect = self.image.get_rect().move(self.pos)
        self.xv = 5
        self.dir = LEFT

    # метод передвижения фона
    def update(self):
        xs = self.xv * tick / 1000
        if self.pos[0] > 0:
            self.dir = LEFT

        if self.pos[0] < -720:
            self.dir = RIGHT

        self.pos[0] += xs * self.dir
        self.rect = self.image.get_rect().move(self.pos)

    # метод отрисовки фона
    def draw(self):
        screen.blit(self.image, self.rect)


# основной класс мяча
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

    # рачитывает коллизию мяча
    # и его дальнейшее передвижение
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
            g.end_screen()

        if pygame.sprite.collide_rect(self, platform):
            self.direction[1] = TOP

    # передвигает мяч в зависимости от тика и скорости мяча
    def move_circle(self, tick):
        xs = self.xv * tick / 1000
        ys = self.yv * tick / 1000

        self.pos = (
            self.pos[0] + self.direction[0] * xs,
            self.pos[1] + self.direction[1] * ys
        )

    # обновляет след, рассчитывает передвижение мяча
    def update(self, tick):
        self.check_collision()
        self.trail.append(Trail(self.pos))
        self.trail = self.trail[-3:]

        for trail in self.trail:
            trail.update()
            trail.draw()

        self.move_circle(tick)
        self.rect = self.image.get_rect().move(self.pos)


# класс, отвечающий за индикацию комбо
class Indicator(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.combo = 0
        self.timer = 1500
        self.pos = (900, 600)

        self.angle = 0
        self.max_angle = 10
        self.min_angle = -7
        self.dir = RIGHT
        self.v = 5

        self.update_image()

    # добавляет к счётчику комбо один пункт
    def add_combo(self):
        self.combo += 1
        self.timer = 1000

    # обнуляет счётчик
    def remove_combo(self):
        self.combo = 0

    # выводит счётчик
    def update_image(self):
        index = 'x' + str(min(self.combo, 6))
        self.image = images['indicators'][index]
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.angle += self.v * tick / 1000 * self.dir

        if self.angle >= self.max_angle:
            self.dir = LEFT
        if self.angle <= self.min_angle:
            self.dir = RIGHT
        print(self.angle)
        self.rect = self.image.get_rect().move(self.pos)

    # удаляет счетчик после определённого времени
    def update(self, *args):
        self.timer -= tick

        if self.timer < 0:
            self.timer = 1500
            self.remove_combo()

        self.update_image()


pygame.init()

# определяет константы
TOP = -1
DOWN = 1

RIGHT = 1
LEFT = -1

SIZE = WIDTH, HEIGHT = 1200, 720

FPS = 120

tick = 0


clock = pygame.time.Clock()

screen = pygame.display.set_mode(SIZE)
colors = pygame.Color
pygame.mouse.set_visible(False)


all_sprites = pygame.sprite.Group()
all_bricks = pygame.sprite.Group()


# подключение всех спрайтов
images = {
    'blue-brick': load_image('images/bricks/blue_brick.png'),
    'blue-brick-damaged': load_image('images/bricks/blue_brick_damaged.png'),
    'red-brick': load_image('images/bricks/red_brick.png'),
    'red-brick-damaged': load_image('images/bricks/red_brick_damaged.png'),
    'ball': load_image('images/ball.png'),
    'ball-hot': load_image('images/ball_hot.png'),
    'platform': load_image('images/platform.png'),
    'background': load_image('images/bg.png'),
    'indicators': {
        'x0': load_image('images/indicators/x0.png'),
        'x1': load_image('images/indicators/x1.png'),
        'x2': load_image('images/indicators/x2.png'),
        'x3': load_image('images/indicators/x3.png'),
        'x4': load_image('images/indicators/x4.png'),
        'x5': load_image('images/indicators/x5.png'),
        'x6': load_image('images/indicators/x6.png')
    }
}

# подключение всех звуков
sounds = {
    'delete': load_sound('sounds/delete.wav'),
    'damage': load_sound('sounds/damage.wav')
}

pole = BrickPole(7, 12)
ball = Ball()
platform = Platform()
bg = Background()
indicator = Indicator()


all_sprites.add(ball)
all_sprites.add(indicator)


# класс, отвечающий за инициализацию игры и заставки
class Game:
    def __init__(self):
        pygame.mixer.music.load('data/sounds/music/bg_music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.25)

    # основной цикл игры
    def main(self):
        update_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEMOTION:
                    platform.move_platform(event.pos[0])
            if len(all_bricks) <= 0:
                self.win_screen()

            global tick
            tick = clock.tick()
            ball.update(tick)
            all_bricks.draw(screen)
            indicator.update()
            all_sprites.draw(screen)

            pygame.display.flip()
            update_screen()

    # пересоздание игры
    def update(self):
        global all_sprites, all_bricks
        all_sprites = pygame.sprite.Group()
        all_bricks = pygame.sprite.Group()

        global pole, ball, platform, bg, indicator
        pole = BrickPole(7, 12)
        ball = Ball()
        platform = Platform()
        bg = Background()
        indicator = Indicator()

        all_sprites.add(ball)
        all_sprites.add(indicator)

    # заставки победы
    def win_screen(self):
        self.fon = pygame.transform.scale(load_image('images/win.png'), (WIDTH, HEIGHT))
        screen.blit(self.fon, (0, 0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                                event.type == pygame.MOUSEBUTTONDOWN:
                    self.main()
            pygame.display.flip()
            clock.tick(FPS)

    # начальная заставка
    def start_screen(self):
        self.fon = pygame.transform.scale(load_image('images/start.png'), (WIDTH, HEIGHT))
        screen.blit(self.fon, (0, 0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                                event.type == pygame.MOUSEBUTTONDOWN:
                    self.update()
                    self.main()
            pygame.display.flip()
            clock.tick(FPS)

    # заставка проигрыша
    def end_screen(self):
        self.fon = pygame.transform.scale(load_image('images/end.png'), (WIDTH, HEIGHT))
        screen.blit(self.fon, (0, 0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                                event.type == pygame.MOUSEBUTTONDOWN:
                    self.update()
                    self.main()
            pygame.display.flip()
            clock.tick(FPS)


if __name__ == '__main__':
    g = Game()
    g.start_screen()