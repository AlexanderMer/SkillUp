import pygame, sys
from pygame.locals import *
from Characters import Player

class Game:
    def __init__(self):
        self.WINDOW_HEIGHT = 600
        self.WINDOW_WIDTH = 800
        pygame.init()
        self.DISPLAY_SURF = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.DOUBLEBUF, 32)
        self.DISPLAY_SURF.fill((0x00, 0xff, 0xff))
        self.characters = [Player(self.DISPLAY_SURF, "Sasha")]
        self.clock = pygame.time.Clock()
        self._main_loop()  # Calls main loop, must be last line!


    def _main_loop(self):
        while True:
            self.DISPLAY_SURF.fill((0x00, 0xff, 0xff))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                pygame.display.update()
            for character in self.characters:
                character.tick()
            pygame.display.flip()
            self.clock.tick(30)

game = Game()
