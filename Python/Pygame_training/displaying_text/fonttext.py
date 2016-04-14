import pygame, sys
from pygame.locals import *


pygame.init()


WINDOW_HEIGHT = 300
WINDOW_WIDTH = 400
MAX_FPS = 30
ticker = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Hello World')

WHITE = (0xff, 0xff, 0xff)
GREEN = (0, 0xff, 0)
BLUE = (0, 0, 0x80)

fontObj = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj = fontObj.render('Hello world!', True, GREEN, BLUE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200, 150)

while True:  # main game loop
    DISPLAYSURF.fill(WHITE)
    textRectObj.center = pygame.mouse.get_pos()
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    ticker.tick(MAX_FPS)

