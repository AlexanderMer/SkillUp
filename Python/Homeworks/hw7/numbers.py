import turtle
#  _      0
# | |    1 2
#  -      3
# |_|    4 5
#         6
#True if line should glow, false otherwise

def draw_fancy(number):
	number = str(int(number))
	offset = 0
	numbers_dic = {
	'0' : (True, True, True, False, True, True, True),
	'1' : (False, False, True, False, False, True, False),
	'2' : (True, False, True, True, True, False, True),
	'3' : (True, False, True, True, False, True, True),
	'4' : (False, True, True, True, False, True, False),
	'5' : (True, True, False, True, False, True, True),
	'6' : (True, True, False, True, True, True, True),
	'7' : (True, False, True, False, False, True, False),
	'8' : (True, True, True, True, True, True, True),
	'9' : (True, True, True, True, False, True, True)
	}

	turtle.bgcolor('Yellow')  
	turtle.color('Red')
	turtle.pu()
	turtle.goto(-400, 100)

	#draw tops horizontall
	for n in number:
		if numbers_dic[n][0]:
			turtle.fd(20)
			turtle.pd()
			turtle.fd(50)
			turtle.pu()
		elif n == '1':
			turtle.fd(20)
		else:
			turtle.fd(70)
			

	#move down to middle and leave a line if needed
	'''if numbers_dic[number[len(number) - 1]][2]:
		turtle.rt(90)
		turtle.pd()
		turtle.fd(50)
		turtle.rt(90)
		turtle.pu()
	else:'''
	turtle.rt(90)
	turtle.fd(50)
	turtle.rt(90)
	

	# draw middles horzontall from right to left
	for n in number[::-1]:
		if numbers_dic[n][3]:
			turtle.pd()
			turtle.fd(50)
			turtle.pu()
			turtle.fd(20)
		elif n == '1':
			turtle.fd(20)
		else:
			turtle.fd(70)

	#move down to bottom and leave a line if needed
	if numbers_dic[number[0]][4]:
		turtle.bk(20)
		turtle.lt(90)
		turtle.pd()
		turtle.fd(50)
		turtle.lt(90)
		turtle.pu()
	elif number[0] == '1' or number[-1] == '1':
		turtle.lt(90)
		turtle.fd(50)
		turtle.lt(90)
		turtle.fd(20)
	else:
		turtle.lt(90)
		turtle.fd(50)
		turtle.lt(90)
	
    # draw bottom horzontall from left to right
	for n in number:
		if numbers_dic[n][6]:
			turtle.pd()
			turtle.fd(50)
			turtle.pu()
			turtle.fd(20)
			offset += 70
		elif n == '1':
			turtle.fd(20)
			offset += 20
		else:
			turtle.fd(70)
			offset += 70

	#return to initial position
	turtle.bk(offset)
	turtle.lt(90)
	turtle.fd(100)
	turtle.rt(180)
	turtle.speed(12)

	#draw all verticals
	for n in number:
		#upper left line
		if numbers_dic[n][1]:
			turtle.pd()
			turtle.fd(50)
			turtle.pu()
		else:
			turtle.fd(50)
		#bottom left line
		if numbers_dic[n][4]:
			turtle.pd()
			turtle.fd(50)
			turtle.pu()
		else:
			turtle.fd(50)

		#move to upper right 
		if n != '1':
			turtle.lt(180 - 26.6)
			turtle.fd(112)
			turtle.rt(63.4 + 90)
		else:
			turtle.bk(100)
			turtle.lt(90)
			turtle.rt(90)

		#upper right line
		if numbers_dic[n][2]:
			turtle.pd()
			turtle.fd(50)
			turtle.pu()
		else:
			turtle.fd(50)

		#botto right line
		if numbers_dic[n][5]:
			turtle.pd()
			turtle.fd(50)
			turtle.pu()
		else:
			turtle.fd(50)
		#move to next number's top left corner
		turtle.lt(180 - 11.3)
		turtle.fd(102)
		turtle.rt(78.7 + 90)


	turtle.exitonclick()

n = input('number ? (integer, please) ')
draw_fancy(n)
