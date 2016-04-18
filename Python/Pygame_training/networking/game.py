import pygame, sys, network_manager, pickle
from pygame.locals import *
from characters import Mage, GuestAvatar
from levels import *

class Game:
    def __init__(self):
        pygame.init()
        # Initiating global vars
        self.clock = pygame.time.Clock()
        self.keys_down = []
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.network = 0  # Network manager instance. Either Server or Client
        self.do_networking = 0  # method which is called every tick
        self.player = 0
        self.players = {}  # Dictionary of other players
        self.players_sprites = 0
        # Setting up window
        self.DISPlAY_SURF = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT),0, 32)
        self.new_game()
        self.__main_loop()  # MUST BE LAST LINE!

    def do_host_networking(self):
        """Must be called every tick if HOSTING game"""
        pass

    def do_client_networking(self):
        """Must be called every tick if game is run in CLIENT mode"""
        self.network.send_message(pickle.dumps(self.player.get_meta_data()))
        print(self.player.get_meta_data()["world_coords"])

    def new_game(self, hosting_game=0):
        # Setting up level
        self.level = Sprite_Level(self.DISPlAY_SURF)
        # Setting up characters Sasha Alex
        my_name = "Sasha" if hosting_game else "Alexander"  # for testing
        self.player = Mage(self.DISPlAY_SURF, self.level, my_name)
        self.players_sprites = pygame.sprite.Group()
        self.players_sprites.add(self.player)
        if hosting_game:
            pygame.display.set_caption("Host")
            self.network = network_manager.Server(self)
            self.do_networking = self.do_host_networking
        else:
            pygame.display.set_caption("Client")
            self.do_networking = self.do_client_networking
            self.world_coords = (256, 256)  # for testing
            self.network = network_manager.Client(self)
            self.network.send_message(pickle.dumps(self.player.get_meta_data()))

    def add_new_player(self, meta_data, conn):
        name = meta_data['name']
        self.players[name] = GuestAvatar(self.DISPlAY_SURF, self.level, name)
        self.players_sprites.add(self.players[meta_data['name']])
        self.players[name].world_coords = meta_data["world_coords"]

    def __main_loop(self):
        while True:
            self.DISPlAY_SURF.fill((0, 0xff, 0xff))
            self.__check_events()  # Check events
            # Update levelsd
            self.level.update()
            # Update player
            for key in self.keys_down:
                self.player.press_key(key)
            self.do_networking()
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
                self.network.close()
                pygame.quit()
                sys.exit()


Game()
