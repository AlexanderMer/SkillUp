import sys
from Level import *


pygame.init()
TICKER = pygame.time.Clock()
# GLOBAL VARS
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
level = Level()

# initiating stuff
pygame.display.set_caption("Tiles")
DISPLAY_SURFACE.fill((0xff, 0xff, 0xff))
level.generate_level()


# MAIN LOOP
while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key in level.ALLOWED_KEYS:
                level.press_key(event.key)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
    level.draw_level(DISPLAY_SURFACE)
    pygame.display.update()
    TICKER.tick(30)
