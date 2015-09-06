from turtle import *
from random import randint, choice, random


flag = 0
def change(wid = 5, angle = 10):	

	while True:
		wid = abs(wid - random() * 0.2)
		angle = angle + randint(1, 5)
		if angle < heading() <= 180:
			direction = right
		elif 180 < heading() < 360 - angle: 
			direction = left
		else:
			direction = right if random() > 0.5 else left
		distance = 15 + random() * 30

		pensize(wid)
		direction(angle)
		forward(distance)

		x, y = position()
	
		global flag
		if random() > 0.8 and flag < 3:
			flag = flag + 1
			print flag
			change(wid=pensize() * 0.5, angle=angle)
			up()
			setx(x)
			sety(y)
			down()

		if x > 300 or y > 300:
			break


color('black', 'yellow')
# right(90)
change()

done()

