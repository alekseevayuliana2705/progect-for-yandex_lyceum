import pygame
from pygame import *
from player import *
from blocks import *
import pyganim
import os


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((width, height_1))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/blocks/platform.png" % rsc)
        self.rect = Rect(x, y, width, height_1)


speed = 7
wight_0 = 22
height_0 = 32
color = "#888888"
for_up = 10
for_down = 0.35
animation = 0.1
rsc = os.path.dirname(__file__)
anim_right = [('%s/mario/r1.png' % rsc),
              ('%s/mario/r2.png' % rsc),
              ('%s/mario/r3.png' % rsc),
              ('%s/mario/r4.png' % rsc),
              ('%s/mario/r5.png' % rsc)]
anim_left = [('%s/mario/l1.png' % rsc),
             ('%s/mario/l2.png' % rsc),
             ('%s/mario/l3.png' % rsc),
             ('%s/mario/l4.png' % rsc),
             ('%s/mario/l5.png' % rsc)]
anim_up_left = [('%s/mario/jl.png' % rsc, 0.1)]
anim_up_rigth = [('%s/mario/jr.png' % rsc, 0.1)]
anim_up = [('%s/mario/j.png' % rsc, 0.1)]
anim_stop = [('%s/mario/0.png' % rsc, 0.1)]


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.x_vert = 0
        self.x_0 = x
        self.y_0 = y
        self.y_vert = 0
        self.ground = False
        self.image = Surface((wight_0, height_0))
        self.image.fill(Color(color))
        self.rect = Rect(x, y, wight_0, height_0)
        self.image.set_colorkey(Color(color))
        sm_anim = []
        for anim in anim_right:
            sm_anim.append((anim, animation))
        self.sm_anim_right = pyganim.PygAnimation(sm_anim)
        self.sm_anim_right.play()
        sm_anim = []
        for anim in anim_left:
            sm_anim.append((anim, animation))
        self.sm_anim_left = pyganim.PygAnimation(sm_anim)
        self.sm_anim_left.play()
        self.sm_anim_stop = pyganim.PygAnimation(anim_stop)
        self.sm_anim_stop.play()
        self.sm_anim_stop.blit(self.image, (0, 0))
        self.sm_anim_up_left = pyganim.PygAnimation(anim_up_left)
        self.sm_anim_up_left.play()
        self.sm_anim_up_right = pyganim.PygAnimation(anim_up_rigth)
        self.sm_anim_up_right.play()
        self.sm_anim_up = pyganim.PygAnimation(anim_up)
        self.sm_anim_up.play()

    def update(self, left, right, up, platforms):
        if up:
            if self.ground:
                self.y_vert = -for_up
            self.image.fill(Color(color))
            self.sm_anim_up.blit(self.image, (0, 0))
        if left:
            self.x_vert = -speed
            self.image.fill(Color(color))
            if up:
                self.sm_anim_up_left.blit(self.image, (0, 0))
            else:
                self.sm_anim_left.blit(self.image, (0, 0))
        if right:
            self.x_vert = speed
            self.image.fill(Color(color))
            if up:
                self.sm_anim_up_right.blit(self.image, (0, 0))
            else:
                self.sm_anim_right.blit(self.image, (0, 0))
        if not (left or right):
            self.x_vert = 0
            if not up:
                self.image.fill(Color(color))
                self.sm_anim_stop.blit(self.image, (0, 0))
        if not self.ground:
            self.y_vert += for_down
        self.ground = False
        self.rect.y += self.y_vert
        self.collide(0, self.y_vert, platforms)
        self.rect.x += self.x_vert
        self.collide(self.x_vert, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.ground = True
                    self.y_vert = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.y_vert = 0


window_weight = 800
window_height = 640
window = (window_weight, window_height)
color_fon = "#004400"


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
    l, t = -l + window_weight / 2, -t + window_height / 2
    l = min(0, l)
    l = max(-(camera.width - window_weight), l)
    t = max(-(camera.height - window_height), t)
    t = min(0, t)
    return Rect(l, t, w, h)


def main():
    pygame.init()
    screen = pygame.display.set_mode(window)
    pygame.display.set_caption("Super Mario Boy")
    bg = Surface((window_weight, window_height))
    bg.fill(Color(color_fon))
    hero = Player(55, 55)
    left = right = False
    up = False
    entities = pygame.sprite.Group()
    platforms = []
    entities.add(hero)
    level = [
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
        "---------------------------------+-",
        "-----------------------------------"]
    timer = pygame.time.Clock()
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            x += width
        y += height_1
        x = 0
    total_level_width = len(level[0]) * width
    total_level_height = len(level) * height_1
    camera = Camera(camera_configure, total_level_width, total_level_height)
    while 1:
        timer.tick(60)
        for e in pygame.event.get():
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
        screen.blit(bg, (0, 0))
        camera.update(hero)
        hero.update(left, right, up, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()


if __name__ == "__main__":
    main()
