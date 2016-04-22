import pygame, sys, network_manager, pickle, logging
from pygame.locals import *
from characters import Mage, GuestAvatar, GuestMage, TYPES_MAP
from levels import *
from network_manager import *

logging.basicConfig(level=logging.DEBUG)
# Latest changes:
# If running in client mode, only GuestAvatar classes should be created
# Each tick Clients send key_presses to Host, which in turn must process them
# After that host sends back the state of game to clients

#TODO Make new classes so guest don't move entire map with htem on host PC!
#TODO Make characters appear in client window
#TODO Make the fucking game!

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
        self.players = {}  # Dictionary of other players, nickname is key
        self.players_sprites = 0  # all players sprites are stored here for rendering
        # Setting up window
        self.DISPlAY_SURF = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT),0, 32)
        self.game_state = 0  # Contains all info about game and players
        self.new_game(hosting)  # Must be last line!


    def do_host_networking(self):
        """Must be called every tick if HOSTING game"""
        self.network.send_to_all(pickle.dumps(Message(network_manager.GAME_STATE, self.collect_players_states())))

    def do_client_networking(self):
        """Must be called every tick if game is run in CLIENT mode"""
        #self.network.send_message(pickle.dumps(Message(network_manager.GAME_STATE, self.player.get_meta_data())))
        self.network.send_message(pickle.dumps(Message(KEYS_PRESSED, (self.player.name, self.keys_down))))

    def new_game(self, hosting_game):
        # Setting up level
        self.level = Sprite_Level(self.DISPlAY_SURF)
        # Setting up characters
        random.seed()
        names = ['Alex', 'Sasha', 'Lekso', 'Sandro', 'Shurka', 'Alexander', 'Aleksander', 'Aleksandre']
        my_name = "Host" if hosting_game else random.choice(names)  # for testing
        self.players_sprites = pygame.sprite.Group()
        if hosting_game:
            self.player = Mage(self.DISPlAY_SURF, self.level, my_name, "Mage")
            pygame.display.set_caption("Host")
            self.network = network_manager.Server(self)
            self.do_networking = self.do_host_networking
            self.players_sprites.add(self.player)
            self._host_main_loop()  # MUST BE LAST LINE!
        else:
            self.player = GuestMage(self.DISPlAY_SURF, self.level, my_name, "Mage")
            pygame.display.set_caption("Client")
            self.do_networking = self.do_client_networking
            self.world_coords = (256, 256)  # for testing
            self.network = network_manager.Client(self)
            # connecting to host
            self.network.send_message(pickle.dumps(Message(network_manager.NEW_PLAYER, self.player.get_meta_data())))
            self.players_sprites.add(self.player)
            self._client_main_loop()  # MUST BE LAST LINE!

    def add_new_player(self, meta_data):
        name = meta_data['name']
        self.players[name] =  TYPES_MAP[meta_data["type"]](self.DISPlAY_SURF, self.level, name, meta_data["type"])
        self.players_sprites.add(self.players[meta_data['name']])
        self.players[name].world_coords = meta_data["world_coords"]
        print("created new player {} -> {}".format(name, self.players[meta_data['name']]))

    def _host_main_loop(self):
        while True:
            self.DISPlAY_SURF.fill((0, 0xff, 0xff))
            self._check_events()  # Check events
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

    def _client_main_loop(self):
        while True:
            self.DISPlAY_SURF.fill((0, 0xff, 0xff))
            self._check_events()  # Check events
            # Update levelsd
            self.level.update()
            # Update player send key presses to server
            self.do_networking()
            self.players_sprites.update()
            self.players_sprites.draw(self.DISPlAY_SURF)
            pygame.display.update()  # Must be last two lines
            self.clock.tick(60)

    def _check_events(self):
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

    def collect_players_states(self):
        game_state = {}
        # for now just collecting world coordinates
        for name in self.players:
            game_state[name] = self.players[name].get_meta_data()
        return game_state


Game()