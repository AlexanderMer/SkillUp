import pygame, sys, network_manager, logging
from pygame.locals import *
from characters import *
from levels import *
from network_manager import *
from game_objects import *

logging.basicConfig(level=logging.DEBUG)
# Latest changes:
# If running in client mode, only GuestAvatar classes should be created
# Each tick Clients send key_presses to Host, which in turn must process them
# After that host sends back the state of game to clients

#TODO Make the fucking game!

class Game:
    def __init__(self, hosting=0):
        pygame.init()
        # Initiating global vars
        self.hosting = hosting
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
        self.DISPlAY_SURF = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.DOUBLEBUF, 32)
        self.game_state = 0  # Contains all info about game and players
        self.crosshair = Crosshair()
        self.game_objects = pygame.sprite.Group()
        self.game_objects.add(self.crosshair)
        self.new_game(hosting)  # Must be last line!

    def do_host_networking(self):
        """Must be called every tick if HOSTING game"""
        self.network.send_to_all(Message(PLAYERS_STATES, self.collect_players_states()))

    def do_client_networking(self):
        """Must be called every tick if game is run in CLIENT mode"""
        self.network.send_message(Message(KEYS_PRESSED, (self.player.name, self.keys_down)))

    def new_game(self, hosting_game):
        # Setting up level
        self.level = Sprite_Level(self.DISPlAY_SURF)
        # Setting up characters
        random.seed()
        my_name = "Host" if hosting_game else str(random.randint(0, 3000))  # for testing
        self.players_sprites = pygame.sprite.Group()
        if hosting_game:
            self.player = Mage(self.DISPlAY_SURF, self.level, my_name, "Mage")
            pygame.display.set_caption("Host")
            self.network = network_manager.GameServer(self)
            self.do_networking = self.do_host_networking
            self.players_sprites.add(self.player)
            self._host_main_loop()  # MUST BE LAST LINE!
        else:
            self.player = Mage(self.DISPlAY_SURF, self.level, my_name, "Mage")
            pygame.display.set_caption("Client {}".format(self.player.name))
            self.do_networking = self.do_client_networking
            self.world_coords = (256, 256)  # for testing
            self.network = network_manager.GameClient(self)
            # connecting to host
            self.network.send_message(Message(network_manager.NEW_PLAYER, self.player.get_meta_data()))
            self.players_sprites.add(self.player)
            self._client_main_loop()  # MUST BE LAST LINE!

    def add_new_player(self, meta_data):
        name = meta_data['name']
        if self.hosting:
            self.players[name] = GuestMage(self.DISPlAY_SURF, self.level, name, meta_data["type"])
        else:
            self.players[name] = GuestMage(self.DISPlAY_SURF, self.level, name, meta_data["type"])
        self.players_sprites.add(self.players[meta_data['name']])
        self.players[name].world_coords = meta_data["world_coords"]
        logging.info("created new player {} -> {}".format(name, self.players[meta_data['name']]))

    def _host_main_loop(self):
        while True:
            #self.DISPlAY_SURF.fill((0, 0xff, 0xff))
            self._check_events()  # Check events like key presses and update global vars
            # Update level
            self.level.update()
            # update crosshair
            self.crosshair.update()
            game_objects.projectiles.draw(self.DISPlAY_SURF)
            self.game_objects.draw(self.DISPlAY_SURF)
            # Update player
            for key in self.keys_down:
                self.player.press_key(key)
            self.do_networking()
            self.players_sprites.update()
            try:
                self.players_sprites.draw(self.DISPlAY_SURF)
            except pygame.error:
                logging.warning("syrface was locked while Blitting")
            #pygame.display.set_caption("Host level_offset: {} {}".format(self.level.x_offset, self.level.y_offset))
            pygame.display.set_caption("w_coords {} {}".format(*self.player.world_coords))
            pygame.display.update()  # Must be last two lines
            self.clock.tick(60)

    def _client_main_loop(self):
        while True:
            #self.DISPlAY_SURF.fill((0, 0xff, 0xff))
            self._check_events()  # Check events
            # Update levelsd
            self.level.update()
            # update crosshair
            self.crosshair.update()
            game_objects.projectiles.draw(self.DISPlAY_SURF)
            self.game_objects.draw(self.DISPlAY_SURF)
            # Update player send key presses to server
            self.do_networking()
            pygame.display.set_caption("{}: {}".format(self.player.name, self.player.world_coords))
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
            elif event.type == pygame.MOUSEBUTTONUP:
                self.crosshair.image.fill((255, 0, 0,))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.crosshair.image.fill((255, 255, 255,))
                self.player.fire_projectile()
                if not self.hosting:
                    velocity = [-((m - r) / 10) for m, r in zip(pygame.mouse.get_pos(), self.player.rect.center)]
                    self.network.send_message(Message(FIRE_PROJECTILE, (self.player.name, velocity,)))
            elif event.type == QUIT:
                logging.info("Quitting game")
                self.network.close()
                pygame.quit()
                sys.exit()

    def collect_players_states(self):
        game_state = []
        # for now just collecting meta data
        game_state.append(self.player.get_meta_data())
        for name in self.players:
            game_state.append(self.players[name].get_meta_data())
        return game_state


Game()