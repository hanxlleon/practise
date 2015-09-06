from turtle import *
from random import randint, random


def change(wid=5, max_angel=10, forwd=40):

    for i in range(forwd):
        
        wid = wid_change(wid)
        forwd = forwd_change(forwd)
        direction, angle = angle_change(max_angel)

        pensize(wid)
        direction(angle)
        forward(forwd)

        x, y = position()

        if random() > 0.7 and wid*random()>2:
            change(wid=pensize() * 0.5, max_angel=40, forwd=15)
            
            up()
            setx(x)
            sety(y)
            down()

        if y < -200 or x > 300:
            break

def angle_change(max_angel=30):
    angle = randint(10, 20)

    left_angle, right_angle = 270 - max_angel, 270 + max_angel

    if 90 < heading() <= left_angle:
        direction = left
    elif right_angle < (heading() % 360) or 0 <= right_angle <= 90:
        direction = right
    else:
        direction = right if random() > 0.5 else left
    
    return (direction, angle)


def forwd_change(forwd):
    forwd = 10 + random() * 15

    return forwd

def wid_change(wid):
    wid = abs(wid - random() * 0.2)

    return wid




up()
sety(300)
down()

right(90)
# change()
for i in range(5):
    change()
    # left(90)
    up()
    setx(-50+random()*250)
    sety(300)
    down()

done()
