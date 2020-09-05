import math
import random
import pyxel
from lib import *

SCREEN_W = 256
SCREEN_H = 240
CENTER_X = SCREEN_W // 2
CENTER_Y = SCREEN_H // 2


def main():

    pyxel.init(SCREEN_W, SCREEN_H)
    pyxel.mouse(True)

    # 中心座標
    vct_center = Vector2(CENTER_X, CENTER_Y)

    # 角度制限の初期値
    limit = math.radians(45)
    rotation = 0

    back_color = 0
    text_color = 0

    while True:

        # 計算基準となるベクトルを作成
        dir_basic = Vector2(1, 0).rotated(math.radians(rotation))
        dir_basic.normalize()

        # 中心からみてマウスの方向を向いているベクトルを作成
        vct_mouse = Vector2(pyxel.mouse_x, pyxel.mouse_y)
        dir_mouse = vct_mouse - vct_center
        dir_mouse.normalize()

        # dir_basicとdir_mouseの角度を計算。
        # angle_toの計算結果はラジアンとして戻ります。
        raw = dir_basic.angle_to(dir_mouse)
        fix = min(max(raw, -limit), limit)

        # 内積の計算。
        # 二つのベクトルの内積を求めると計算相手の向き（前後）を調べることが出来ます。
        dot = dir_basic.dot(dir_mouse)
        # 外積を計算。
        # 二つのベクトルの外積を求めると計算相手の向き（左右）を調べることが出来ます。
        crs = dir_basic.cross(dir_mouse)

        if pyxel.btnp(pyxel.KEY_SPACE) == 1:
            rotation = 0
            limit = math.radians(45)

        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) == 1:
            rotation += 15
            if rotation == 360:
                rotation = 0

        if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON) == 1:
            limit = abs(raw)

        back_color = 0
        if abs(raw) > limit:
            back_color = 1

        text_color = 7
        if dot < 0:
            text_color = 8

        # 描画処理部
        pyxel.cls(back_color)

        pyxel.line(
            CENTER_X,
            CENTER_Y,
            CENTER_X + dir_basic.x * 64,
            CENTER_Y + dir_basic.y * 64,
            5,
        )

        vct_calc = dir_basic.rotated(fix)
        pyxel.line(
            CENTER_X,
            CENTER_Y,
            CENTER_X + vct_calc.x * 64,
            CENTER_Y + vct_calc.y * 64,
            12,
        )

        vct_calc = dir_basic.rotated(raw)
        pyxel.line(
            CENTER_X,
            CENTER_Y,
            CENTER_X + dir_mouse.x * 64,
            CENTER_Y + dir_mouse.y * 64,
            7,
        )

        list_text = [
            "     mouse: {:7.2f} {:7.2f}".format(pyxel.mouse_x, pyxel.mouse_y),
            " dir_mouse: {:7.2f} {:7.2f}".format(dir_mouse.x, dir_mouse.y),
            "angle(rad): {:7.2f}".format(raw),
            "angle(deg): {:7.2f}".format(math.degrees(raw)),
            "       dot: {:7.2f} [{:5s}]".format(dot, "front" if dot > 0 else "back"),
            "     cross: {:7.2f} [{:5s}]".format(crs, "right" if crs > 0 else "left"),
            "     frame: {:4d}".format(pyxel.frame_count),
        ]
        for n, text in enumerate(list_text):
            pyxel.text(8, 8 * n + 8, text, text_color)

        pyxel.text(8, 208, "  rotation: {:4d}".format(rotation), 5)
        pyxel.text(8, 216, "limit(rad): {:7.2f}".format(limit), 12)
        pyxel.text(8, 224, "limit(deg): {:7.2f}".format(math.degrees(limit)), 12)

        pyxel.flip()


if __name__ == "__main__":
    main()


# [EOF]