import pygame, sys
from pygame.locals import *
from characters import Mage, GuestAvatar
from levels import *


class Game:
    def __init__(self):
        pygame.init()
        # Initiating global vars
        self.clock = pygame.time.Clock()
        self.keys_down = []
        # Setting up window
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.DISPlAY_SURF = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT),0, 32)
        pygame.display.set_caption('Level collisions')
        # Setting up level
        self.level = Sprite_Level(self.DISPlAY_SURF)
         # Setting up characters
        self.player = Mage(self.DISPlAY_SURF, self.level, "Sasha")
        self.player2 = GuestAvatar(self.DISPlAY_SURF, self.level, "Dima")
        self.player2.world_coords = 100, 100
        self.players_sprites = pygame.sprite.Group()
        self.players_sprites.add(self.player)
        self.players_sprites.add(self.player2)


        self.__main_loop()  # MUST BE LAST LINE!

    def __main_loop(self):
        while True:
            self.DISPlAY_SURF.fill((0, 0xff, 0xff))
            self.__check_events()  # Check events
            # Update levelsd
            self.level.update()
            # Update player
            for key in self.keys_down:
                self.player.press_key(key)
            self.players_sprites.update()
            self.players_sprites.draw(self.DISPlAY_SURF)
            pygame.display.update()  # Must be last two lines
            self.clock.tick(60)

    def __check_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                self.keys_down.append(event.key)
            elif event.type == KEYUP:
                self.keys_down.remove(event.key)
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()


Game()
