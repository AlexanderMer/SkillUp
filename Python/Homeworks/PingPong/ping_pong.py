from tkinter import *
from random import *

#  global vars
BOARD_HEIGHT = 400
BOARD_WIDTH = 800
BALL_X = 10
BALL_Y = 10
PLAYER_STEP = 20
PING_SPEED = 0
PONG_SPEED = 0
root = Tk()

def set_up_board():
	global GAME_BOARD
	global PING_TEXT
	global PONG_TEXT
	global BALL
	global BALL_SIZE
	global REC_WIDTH
	global REC_HEIGHT
	global PING
	global PONG
	GAME_BOARD = Canvas(root, width=BOARD_WIDTH, height=BOARD_HEIGHT, bg="green")
	GAME_BOARD.grid()
	REC_WIDTH = int(BOARD_WIDTH / 100)
	REC_HEIGHT = int(BOARD_HEIGHT / 5)
	#  setting up ping
	PING = GAME_BOARD.create_rectangle(0, 0, REC_WIDTH, REC_HEIGHT, fill="yellow")
	GAME_BOARD.create_line(REC_WIDTH, 0, REC_WIDTH, BOARD_HEIGHT,  fill="white")
	#  setting up pong
	PONG = GAME_BOARD.create_rectangle(BOARD_WIDTH - REC_WIDTH, 0,  BOARD_WIDTH, REC_HEIGHT, fill="yellow")
	GAME_BOARD.create_line(BOARD_WIDTH - REC_WIDTH, 0, BOARD_WIDTH - REC_WIDTH, BOARD_HEIGHT,  fill="white")
	#  line and circle in between
	half_width = int(BOARD_WIDTH / 2)
	half_height = int(BOARD_HEIGHT / 2)
	circle_rad = int(BOARD_WIDTH / 85)
	GAME_BOARD.create_line(half_width, 0, half_width, BOARD_HEIGHT, fill="white")
	GAME_BOARD.create_oval(half_width - circle_rad, half_height - circle_rad,
						half_width + circle_rad, half_height + circle_rad, fill="white", outline="white")
	#  score texts
	PING_TEXT = GAME_BOARD.create_text(int(BOARD_WIDTH / 15), int(BOARD_HEIGHT / 18),text="0", font="Arial 20", fill="white")
	PONG_TEXT = GAME_BOARD.create_text(BOARD_WIDTH - int(BOARD_WIDTH / 15), int(BOARD_HEIGHT / 18),text="0", font="Arial 20", fill="white")
	#  ball
	BALL_SIZE = int(BOARD_HEIGHT / 30)
	x, y = randint(0, BOARD_WIDTH), randint(0, BOARD_HEIGHT)
	BALL = GAME_BOARD.create_oval(x - BALL_SIZE, y - BALL_SIZE, x + BALL_SIZE, y + BALL_SIZE, fill="white")
	#  binding keys
	GAME_BOARD.focus_set()
	GAME_BOARD.bind('<KeyPress>', pressed)
	GAME_BOARD.bind('<KeyRelease>', released)
	
	
def move_stuff():
	global BALL_X
	global BALL_Y
	#  Move ball
	GAME_BOARD.move(BALL, BALL_X, BALL_Y)
	ball_coords = GAME_BOARD.coords(BALL)
	ping_coords = GAME_BOARD.coords(PING)
	pong_coords = GAME_BOARD.coords(PONG)
	#  check in which half of board the ball
	if ball_coords[0] < BOARD_WIDTH / 2:
		if ping_coords[1] < ball_coords[1] < ping_coords[3]:
			print("range!")
	else:
		if pong_coords[1] < ball_coords[3] < pong_coords[3]:
			print("!!!!!!!!!!")

	if  not (0 < ball_coords[1] < BOARD_HEIGHT - 1):
				BALL_Y = -BALL_Y
				print("switched direction")
	if not (15 < ball_coords[0] < BOARD_WIDTH - 30):
		BALL_X = -BALL_X
		print("switched direction")
	

	#  Move player
	if 0 <= ping_coords[3] - REC_HEIGHT / 2 + PING_SPEED <= BOARD_HEIGHT:
		GAME_BOARD.move(PING, 0,PING_SPEED)
	if 0 <= pong_coords[3] - REC_HEIGHT / 2 + PONG_SPEED <= BOARD_HEIGHT:
		GAME_BOARD.move(PONG, 0, PONG_SPEED)
	root.after(50, move_stuff)

def pressed(event):
	global PING_SPEED , PONG_SPEED
	if event.keysym == 'w':
		PING_SPEED = -PLAYER_STEP
	elif event.keysym == 's':
		PING_SPEED = PLAYER_STEP
	elif event.keysym == 'Up':
		PONG_SPEED = -PLAYER_STEP
	elif event.keysym == 'Down':
		PONG_SPEED = PLAYER_STEP

def released(event):
	global PING_SPEED, PONG_SPEED
	if event.keysym in "ws":
		PING_SPEED = 0
	elif event.keysym == "Down" or event.keysym == "Up":
		PONG_SPEED = 0


def start_game():
	move_stuff()

set_up_board()
start_game()
root.mainloop()