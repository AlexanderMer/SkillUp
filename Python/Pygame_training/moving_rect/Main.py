import pygame, sys
from pygame.locals import *
from Level import Level
from Characters import Player


pygame.init()
level = Level()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption("moving rect")
ticker = pygame.time.Clock()
WINDOW.fill((0xff, 0xff, 0xff))
player = Player(WINDOW)
WINDOW.blit(WINDOW, player)
keys_down = []
margin = 50

def check_pos():
    if player.x >= WINDOW_WIDTH - margin:
        level.move_map((-player.step_size, 0))
    if player.x <= margin:
        level.move_map((player.step_size, 0))
    if player.y >= WINDOW_HEIGHT - margin:
        level.move_map((0, -player.step_size))
    if player.y <= margin:
        level.move_map((0, player.step_size))

# MAIN LOOP
while True:
    level.draw_level(WINDOW)
    pygame.draw.rect(WINDOW, (0xff, 0, 0), player)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key not in keys_down:
                keys_down.append(event.key)
        elif event.type == KEYUP:
            keys_down.remove(event.key)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
    for key in keys_down:
        player.press_key(key)
    check_pos()
    player.move((0, 0))
    pygame.display.update()
    ticker.tick(30)
