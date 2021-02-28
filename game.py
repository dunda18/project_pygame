import pygame
import random
import time
import sqlite3


data_base = sqlite3.connect("top_db.sqlite")
cur = data_base.cursor()

user = cur.execute('SELECT user from cur_user').fetchall()[0][0]

# level = str(cur.execute('SELECT level FROM users WHERE login = ?', (user,)).fetchone()[0])
# print(level)

pygame.init()

W = 600
H = 700
screen = pygame.display.set_mode([W, H])

WHITE = (255, 255, 255)
GREY = (160, 160, 160)

car_w = 75
car_h = 100
x = W // 2 - car_w // 2
y = H - 225

pol1_x = W // 3 - 10
pol1_y = 0
pol2_x = 2 * W // 3 - 10
pol2_y = 0

money_w = 75
money_h = 75


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (car_w, car_h))
        self.rect = self.image.get_rect(
            topleft=(x, y))
        self.default_x = x
        self.default_y = y

    def draw(self):
        screen.blit(self.image, self.rect)

    def default_pos(self):
        self.rect.x = self.default_x
        self.rect.y = self.default_y

    def move_right(self):
        self.rect.x += W // 3
        if self.rect.x > W:
            self.rect.x -= W // 3

    def move_left(self):
        self.rect.x -= W // 3
        if self.rect.x < 0:
            self.rect.x += W // 3


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, filename, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (car_w, car_h))
        self.rect = self.image.get_rect(
            topleft=(x, y))
        self.y = y
        self.speed = speed

    def update(self):
        self.rect.y = self.y
        self.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)


class Money(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (money_w, money_h))
        self.rect = self.image.get_rect(
            topleft=(x, y))
        self.y = y
        self.speed = random.choice((0.5, 0.6))

    def update(self):
        self.rect.y = self.y
        self.y += self.speed
        if self.rect.y > H:
            self.kill()

    def draw(self):
        screen.blit(self.image, self.rect)


class Pol(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = random.choice((0.3,))

    def update(self):
        self.y += self.speed
        if self.y > H:
            self.y = -100

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, 20, 100))


font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip().split(" ") for line in mapFile]

    return level_map


car = Player(x, y, 'car' + str(cur.execute('SELECT select_car FROM users WHERE login = ?', (user,)).fetchall()[0][0]
                               + 3) + '.png')

t = 0
col = 0

moneys = pygame.sprite.Group()
cars = pygame.sprite.Group()
pols = pygame.sprite.Group()

cur_y = 0
while cur_y < H:
    pol_1 = Pol(pol1_x, cur_y)
    pols.add(pol_1)
    pol_2 = Pol(pol2_x, cur_y)
    pols.add(pol_2)
    cur_y += 200

score = 0
level_cnt = cur.execute('SELECT level FROM users WHERE login = ?', (user,)).fetchall()[0][0]
if level_cnt > 10:
    level_cnt = 10
car_cnt = 0
level = 0
last_level_end = 1
pass_flag = 0
t_end = 0

eps = 1.5


running = True
while running:
    if level_cnt >= 7:
        eps = 1
    if level_cnt >= 10:
        eps = 0.7
    if time.time() - t > eps:
        t = time.time()

        if t - t_end >= 5 and pass_flag == 1:
            last_level_end = 1
            car_cnt = 0
            pass_flag = 0
            level_cnt += 1

            cur.execute('UPDATE users SET level = ? WHERE login = ?', (level_cnt, user))
            cur.execute('UPDATE users SET coins = ? WHERE login = ?', (score + cur.execute('''SELECT coins FROM
             users WHERE login = ?''', (user,)).fetchall()[0][0], user))
            data_base.commit()

            score = 0

        if last_level_end:
            level = load_level("Level_" + str(level_cnt) + ".txt")
            last_level_end = 0

        if car_cnt >= len(level) and pass_flag == 0:
            pass_flag = 1
            t_end = t

        if pass_flag == 0:

            color = random.randint(1, 3)
            do_money = random.randint(1, 2)
            col = int(level[car_cnt][0]) - 1
            speed = float(level[car_cnt][1])
            car_cnt += 1

            car1 = Car(W // 3 * col + (W - 40) // 6 - car_w / 2 + col // 2 * 10 + (col == 1) * 7, -car_h,
                       'car' + str(color) + '.png', speed)
            cars.add(car1)

            if do_money == 2:
                money_col = random.randint(0, 2)
                while money_col == col:
                    money_col = random.randint(0, 2)

                money = Money(W // 3 * money_col + (W - 40) // 6 - car_w / 2 + money_col // 2 * 10 + (money_col == 1)
                              * 7, -money_h,
                              'money.png')

                moneys.add(money)

    hits_money = pygame.sprite.spritecollide(car, moneys, True)
    hits_car = pygame.sprite.spritecollide(car, cars, True)

    if hits_car:
        cur.execute('UPDATE users SET coins = ? WHERE login = ?', (score + cur.execute('''SELECT coins FROM
                     users WHERE login = ?''', (user,)).fetchall()[0][0], user))
        data_base.commit()

        score = 0

        for car1 in cars:
            car1.kill()
        for money in moneys:
            money.kill()

        car.default_pos()

        car_cnt = 0
        pass_flag = 0

    for hit in hits_money:
        score += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car.move_left()
            if event.key == pygame.K_RIGHT:
                car.move_right()

    screen.fill(GREY)

    for pol in pols:
        pol.draw()
    car.draw()
    cars.draw(screen)
    moneys.draw(screen)

    cars.update()
    moneys.update()
    pols.update()

    draw_text(screen, 'Score: ' + str(score), 18, 30, 5)
    draw_text(screen, 'Level: ' + str(level_cnt), 18, W - 30, 5)

    pygame.display.flip()

    # pygame.time.delay(20)

pygame.quit()