# -*- coding: utf-8 -*-
from turtle import *
from random import randint, random


def lightning(wid=5, max_angle=10, forwd_count=40):
    """
    :param wid: 画笔宽度
    :param max_angle: 画笔与-y轴的最大夹角，超过夹角则向相反方向移动
    :param forwd_count: 前进的次数
    """

    for i in range(forwd_count):
        wid = wid_change(wid)
        forwd = forwd_change()
        direction, angle = angle_change(max_angle)

        pensize(wid)
        direction(angle)
        forward(forwd)

        x, y = position()

        # 生成分叉
        if random() > 0.7 and wid * random() > 2:
            lightning(wid=pensize() * 0.5, max_angle=40, forwd_count=15)

            up()
            setx(x)
            sety(y)
            down()

        # 结束
        if y < -200:
            break


def angle_change(max_angle=30):
    """角度和转向变化"""

    angle = randint(10, 20)  # 角度变化

    max_angle = min(max_angle, 90)  # 闪电向下走，与-y轴的夹角不大于90度
    left_angle, right_angle = 270 - max_angle, 270 + max_angle

    if 90 < heading() <= left_angle:  # 如果过于偏左（y轴左侧超过max_angle），则下一次往右侧转（以画笔为视角则是向左转）
        direction = left
    elif right_angle < heading() or 0 <= heading() <= 90:
        direction = right
    else:
        direction = right if random() > 0.5 else left

    return (direction, angle)


def forwd_change(forwd=10):
    """步进距离变化"""

    forwd = forwd + random() * 15

    return forwd


def wid_change(wid):
    """宽度变化"""

    wid = abs(wid - random() * 0.2)

    return wid


if __name__ == '__main__':
    up()
    sety(300)
    down()

    right(90)
    lightning()
    # for i in range(5):
    #     lightning()
    #     up()
    #     setx(-50+random()*250)
    #     sety(300)
    #     down()

    done()
