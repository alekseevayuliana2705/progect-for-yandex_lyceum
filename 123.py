import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import pygame
from pygame import *
from player import *
from blocks import *
import pyganim
import os


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('proj.ui', self)  # Загружаем дизайн
        self.lev_plan = []
        self.pushButton.clicked.connect(self.lev_1)
        self.pushButton2.clicked.connect(self.lev_2)

    def lev_1(self):
        self.lev_plan = [
            "-----------------------------------",
            "-  --------------------------------",
            "-        -        -   -   -       -",
            "--------   ------   -   -   ----- -",
            "-  -   ----- -  --------- - -   - -",
            "-    -            -     -*-   - - -",
            "- ------ -  -  -     -    ------- -",
            "-     ---------------------     - -",
            "---                       - --- - -",
            "----------------------  ---   -   -",
            "-                       ----- -----",
            "- -----------------------     -   -",
            "-                    -  --- -   - -",
            "-------------------- -    - ----- -",
            "-      -------------*- -- -     - -",
            "---- ---         -   - -  ----- - -",
            "---- -   -----   - --- - --   -   -",
            "---- - ---   --- - -   -    - -----",
            "---- - -   -   - - - -------- -   -",
            "----   - -----   - -          - - -",
            "--------     ----- ------------ - -",
            "----   -----   -   -     -      - -",
            "---- -     --- - --- --- - ------ -",
            "---- -----     - -   -   - -   -  -",
            "---- -   ------- - --- --- - - - --",
            "---- - - -   -   -   -     - - -  -",
            "---- - - - - - ----- - ----- - -- -",
            "----   -   - -       -       -  - -",
            "--------------------------------- -",
            "-----------------------------------"
        ]

    def lev_2(self):
        self.lev_plan = [
            "-----------------------------------",
            "-                                 -",
            "-       ----------                -",
            "-                                 -",
            "-                    -------      -",
            "-  ----                           -",
            "-                                 -",
            "-                                 -",
            "-             --------        -----",
            "-                                 -",
            "-                                 -",
            "-                          ----   -",
            "-    ---                          -",
            "-                                 -",
            "-           --                    -",
            "-                                 -",
            "-                                 -",
            "-              -----------        -",
            "-                                 -",
            "-                                 -",
            "-        ---                      -",
            "-                                 -",
            "-----------------------------------"
        ]

        class Platform(sprite.Sprite):
            def __init__(self, x, y):
                sprite.Sprite.__init__(self)
                self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                self.image.fill(Color(PLATFORM_COLOR))
                self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
                self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

        MOVE_SPEED = 7
        WIDTH = 22
        HEIGHT = 32
        COLOR = "#888888"
        JUMP_POWER = 10
        GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз
        ANIMATION_DELAY = 0.1  # скорость смены кадров
        ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

        ANIMATION_RIGHT = [('%s/mario/r1.png' % ICON_DIR),
                           ('%s/mario/r2.png' % ICON_DIR),
                           ('%s/mario/r3.png' % ICON_DIR),
                           ('%s/mario/r4.png' % ICON_DIR),
                           ('%s/mario/r5.png' % ICON_DIR)]
        ANIMATION_LEFT = [('%s/mario/l1.png' % ICON_DIR),
                          ('%s/mario/l2.png' % ICON_DIR),
                          ('%s/mario/l3.png' % ICON_DIR),
                          ('%s/mario/l4.png' % ICON_DIR),
                          ('%s/mario/l5.png' % ICON_DIR)]
        ANIMATION_JUMP_LEFT = [('%s/mario/jl.png' % ICON_DIR, 0.1)]
        ANIMATION_JUMP_RIGHT = [('%s/mario/jr.png' % ICON_DIR, 0.1)]
        ANIMATION_JUMP = [('%s/mario/j.png' % ICON_DIR, 0.1)]
        ANIMATION_STAY = [('%s/mario/0.png' % ICON_DIR, 0.1)]

        class Player(sprite.Sprite):
            def __init__(self, x, y):
                sprite.Sprite.__init__(self)
                self.xvel = 0  # скорость перемещения. 0 - стоять на месте
                self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
                self.startY = y
                self.yvel = 0  # скорость вертикального перемещения
                self.onGround = False  # На земле ли я?
                self.image = Surface((WIDTH, HEIGHT))
                self.image.fill(Color(COLOR))
                self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
                self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
                #        Анимация движения вправо
                boltAnim = []
                for anim in ANIMATION_RIGHT:
                    boltAnim.append((anim, ANIMATION_DELAY))
                self.boltAnimRight = pyganim.PygAnimation(boltAnim)
                self.boltAnimRight.play()
                #        Анимация движения влево
                boltAnim = []
                for anim in ANIMATION_LEFT:
                    boltAnim.append((anim, ANIMATION_DELAY))
                self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
                self.boltAnimLeft.play()

                self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
                self.boltAnimStay.play()
                self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

                self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
                self.boltAnimJumpLeft.play()

                self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
                self.boltAnimJumpRight.play()

                self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
                self.boltAnimJump.play()

            def update(self, left, right, up, platforms):

                if up:
                    if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                        self.yvel = -JUMP_POWER
                    self.image.fill(Color(COLOR))
                    self.boltAnimJump.blit(self.image, (0, 0))

                if left:
                    self.xvel = -MOVE_SPEED  # Лево = x- n
                    self.image.fill(Color(COLOR))
                    if up:  # для прыжка влево есть отдельная анимация
                        self.boltAnimJumpLeft.blit(self.image, (0, 0))
                    else:
                        self.boltAnimLeft.blit(self.image, (0, 0))

                if right:
                    self.xvel = MOVE_SPEED  # Право = x + n
                    self.image.fill(Color(COLOR))
                    if up:
                        self.boltAnimJumpRight.blit(self.image, (0, 0))
                    else:
                        self.boltAnimRight.blit(self.image, (0, 0))

                if not (left or right):  # стоим, когда нет указаний идти
                    self.xvel = 0
                    if not up:
                        self.image.fill(Color(COLOR))
                        self.boltAnimStay.blit(self.image, (0, 0))

                if not self.onGround:
                    self.yvel += GRAVITY

                self.onGround = False;  # Мы не знаем, когда мы на земле((
                self.rect.y += self.yvel
                self.collide(0, self.yvel, platforms)

                self.rect.x += self.xvel  # переносим свои положение на xvel
                self.collide(self.xvel, 0, platforms)

            def collide(self, xvel, yvel, platforms):
                for p in platforms:
                    if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                        if xvel > 0:  # если движется вправо
                            self.rect.right = p.rect.left  # то не движется вправо

                        if xvel < 0:  # если движется влево
                            self.rect.left = p.rect.right  # то не движется влево

                        if yvel > 0:  # если падает вниз
                            self.rect.bottom = p.rect.top  # то не падает вниз
                            self.onGround = True  # и становится на что-то твердое
                            self.yvel = 0  # и энергия падения пропадает

                        if yvel < 0:  # если движется вверх
                            self.rect.top = p.rect.bottom  # то не движется вверх
                            self.yvel = 0  # и энергия прыжка пропадает

        # Объявляем переменные
        WIN_WIDTH = 800  # Ширина создаваемого окна
        WIN_HEIGHT = 640  # Высота
        DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
        BACKGROUND_COLOR = "#004400"

        class Camera(object):
            def __init__(self, camera_func, width, height):
                self.camera_func = camera_func
                self.state = Rect(0, 0, width, height)

            def apply(self, target):
                return target.rect.move(self.state.topleft)

            def update(self, target):
                self.state = self.camera_func(self.state, target.rect)

        def camera_configure(camera, target_rect):
            l, t, _, _ = target_rect
            _, _, w, h = camera
            l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

            l = min(0, l)  # Не движемся дальше левой границы
            l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
            t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
            t = min(0, t)  # Не движемся дальше верхней границы

            return Rect(l, t, w, h)

        def main():
            pygame.init()  # Инициация PyGame, обязательная строчка
            screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
            pygame.display.set_caption("Super Mario Boy")  # Пишем в шапку
            bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
            # будем использовать как фон
            bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

            hero = Player(55, 55)  # создаем героя по (x,y) координатам
            left = right = False  # по умолчанию - стоим
            up = False

            entities = pygame.sprite.Group()  # Все объекты
            platforms = []  # то, во что мы будем врезаться или опираться

            entities.add(hero)

            level = self.lev_plan

            timer = pygame.time.Clock()
            x = y = 0  # координаты
            for row in level:  # вся строка
                for col in row:  # каждый символ
                    if col == "-":
                        pf = Platform(x, y)
                        entities.add(pf)
                        platforms.append(pf)

                    x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
                y += PLATFORM_HEIGHT  # то же самое и с высотой
                x = 0  # на каждой новой строчке начинаем с нуля

            total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
            total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

            camera = Camera(camera_configure, total_level_width, total_level_height)

            while 1:  # Основной цикл программы
                timer.tick(60)
                for e in pygame.event.get():  # Обрабатываем события
                    if e.type == QUIT:
                        raise SystemExit
                    if e.type == KEYDOWN and e.key == K_UP:
                        up = True
                    if e.type == KEYDOWN and e.key == K_LEFT:
                        left = True
                    if e.type == KEYDOWN and e.key == K_RIGHT:
                        right = True

                    if e.type == KEYUP and e.key == K_UP:
                        up = False
                    if e.type == KEYUP and e.key == K_RIGHT:
                        right = False
                    if e.type == KEYUP and e.key == K_LEFT:
                        left = False

                screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

                camera.update(hero)  # центризируем камеру относительно персонажа
                hero.update(left, right, up, platforms)  # передвижение
                # entities.draw(screen) # отображение
                for e in entities:
                    screen.blit(e.image, camera.apply(e))

                pygame.display.update()  # обновление и вывод всех изменений на экран

        if __name__ == "__main__":
            main()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())