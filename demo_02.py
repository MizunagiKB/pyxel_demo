import math
import random
import pyxel
from lib import *

SCREEN_W = 256
SCREEN_H = 240

list_render = []
list_laser = []
list_enemy = []
list_crash = []


class CEnemy:
    SIZE = 16

    def __init__(self, vct_position):
        self.vct_position = vct_position
        self.speed = random.randint(1, 6)
        self.enable = True

    def update(self):
        if self.vct_position.y < (SCREEN_H + self.SIZE):
            list_render.append(self)
        else:
            self.enable = False

        self.vct_position.y += self.speed

    def render(self):
        pyxel.rect(
            self.vct_position.x - 8, self.vct_position.y - 8, self.SIZE, self.SIZE, 13
        )


class CCrash:
    COLOR = [10, 9, 8, 10]
    LIMIT = 5

    def __init__(self, vct_position):
        self.vct_position = vct_position
        self.counter = 0
        self.enable = True

    def update(self):
        if self.counter < self.LIMIT:
            list_render.append(self)
        else:
            self.enable = False
        self.counter += 1

    def render(self):
        try:
            col = self.COLOR[self.counter]
        except:
            col = self.COLOR[-1]

        pyxel.circ(
            self.vct_position.x,
            self.vct_position.y,
            math.sin(math.radians(self.counter)) * SCREEN_W,
            col,
        )


class CLaser:
    COLOR = [7, 6, 12, 5, 1]
    LIMIT = 90
    LINE_SIZE = 8

    def __init__(self, vct_position):
        self.vct_position = vct_position
        self.list_position = []
        self.vct_direction = Vector2(0, -1)
        self.speed = 4
        self.deg_limit = 2
        self.counter = 0
        self.enable = True

    def set_target(self, vct_target):
        self.vct_target = vct_target

    def update(self):
        global list_enemy

        v = self.vct_target - self.vct_position

        for enemy in list_enemy:
            if enemy.enable is True:
                if (enemy.vct_position - self.vct_position).length() < CEnemy.SIZE:
                    list_crash.append(
                        CCrash(Vector2(self.vct_position.x, self.vct_position.y))
                    )
                    enemy.enable = False
                    self.enable = False

        v.normalize()
        r = self.vct_direction.angle_to(v)

        if self.counter > 15:
            self.deg_limit = 30
            self.speed = 16
        elif self.counter > (self.LIMIT - 30):
            self.deg_limit = 90

        minr = math.radians(self.deg_limit)
        maxr = math.radians(-self.deg_limit)
        r = min(max(r, maxr), minr)

        self.vct_direction = self.vct_direction.rotated(r)
        self.vct_direction.normalize()

        self.vct_position += self.vct_direction * self.speed

        self.list_position.insert(0, Vector2(self.vct_position.x, self.vct_position.y))
        if len(self.list_position) > self.LINE_SIZE:
            self.list_position = self.list_position[0 : self.LINE_SIZE]

        if self.counter < self.LIMIT:
            list_render.append(self)
        else:
            self.enable = False
        self.counter += 1

    def render(self):

        x1 = self.list_position[0].x
        y1 = self.list_position[0].y

        for n, o in enumerate(self.list_position):

            try:
                col = self.COLOR[n]
            except:
                col = self.COLOR[-1]

            pyxel.line(x1, y1, o.x, o.y, col)
            x1 = o.x
            y1 = o.y


def main():
    global list_render
    global list_laser
    global list_crash
    global list_enemy

    pyxel.init(SCREEN_W, SCREEN_H)
    pyxel.mouse(True)

    while True:
        pyxel.cls(0)

        if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
            o = CLaser(Vector2(random.randint(0, SCREEN_W), SCREEN_W))
            list_laser.append(o)

        o = CEnemy(Vector2(random.randint(0, SCREEN_W), -CEnemy.SIZE))
        list_enemy.append(o)

        for o in list_enemy:
            o.update()

        for o in list_laser:
            o.set_target(Vector2(pyxel.mouse_x, pyxel.mouse_y))
            o.update()

        for o in list_crash:
            o.update()

        [o.render() for o in list_render]

        pyxel.text(8, 8, "Render(s) {:4d}".format(len(list_render)), 7)
        pyxel.text(8, 16, "Enemy(s)  {:4d}".format(len(list_enemy)), 7)
        pyxel.text(8, 24, "Laser(s)  {:4d}".format(len(list_laser)), 7)
        pyxel.text(8, 32, "Crash(s)  {:4d}".format(len(list_crash)), 7)

        list_enemy = [o for o in list_enemy if o.enable is True]
        list_laser = [o for o in list_laser if o.enable is True]
        list_crash = [o for o in list_crash if o.enable is True]
        list_render = []

        pyxel.flip()


if __name__ == "__main__":
    main()


# [EOF]
