import pygame, sys, characters
from pygame.locals import *
from levels import Level


class Game:

    def __init__(self):
        pygame.init()
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.DISPlAY_SURF = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.DOUBLEBUF, 32)
        self.clock = pygame.time.Clock()
        self.players = pygame.sprite.Group()
        self.player = characters.Mage(self.DISPlAY_SURF, "Sasha")
        self.players.add(self.player)
        self.keys_down = []
        self.level = Level(self.DISPlAY_SURF, [self.player])
        self._main_loop()  # Must be last line!



    def _main_loop(self):
        while True:
            self.DISPlAY_SURF.fill((25, 255, 255))
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self.keys_down.append(event.key)
                elif event.type == KEYUP:
                    self.keys_down.remove(event.key)
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            for key in self.keys_down:
                self.player.press_key(key)
            self.level.update()
            self.level.draw_level()
            self.players.update()
            self.players.draw(self.DISPlAY_SURF)
            pygame.display.update()
            self.clock.tick(60)

Game()
