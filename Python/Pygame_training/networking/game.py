import pygame, sys, network_manager, pickle, logging
from pygame.locals import *
from characters import Mage, GuestAvatar, GuestMage, TYPES_MAP
from levels import *

logging.basicConfig(level=logging.DEBUG)

class Game:
    def __init__(self, hosting=0):
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
        self.new_game(hosting)
        self.__main_loop()  # MUST BE LAST LINE!

    def do_host_networking(self):
        """Must be called every tick if HOSTING game"""
        pass

    def do_client_networking(self):
        """Must be called every tick if game is run in CLIENT mode"""
        self.network.send_message(pickle.dumps(self.player.get_meta_data()))

    def new_game(self, hosting_game):
        # Setting up level
        self.level = Sprite_Level(self.DISPlAY_SURF)
        # Setting up characters
        random.seed()
        names = ['Alex', 'Sasha', 'Lekso', 'Sandro', 'Shurka', 'Alexander', 'Aleksander', 'Aleksandre']
        my_name = "Host" if hosting_game else random.choice(names)  # for testing
        self.player = Mage(self.DISPlAY_SURF, self.level, my_name, "Mage")
        self.players_sprites = pygame.sprite.Group()
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
        self.players_sprites.add(self.player)

    def add_new_player(self, meta_data, conn):
        name = meta_data['name']
        self.players[name] =  TYPES_MAP[meta_data["type"]](self.DISPlAY_SURF, self.level, name, meta_data["type"])
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
                if event.key in self.keys_down:
                    self.keys_down.remove(event.key)
            elif event.type == QUIT:
                logging.info("Quitting game")
                #self.network.close()
                pygame.quit()
                sys.exit()


Game()