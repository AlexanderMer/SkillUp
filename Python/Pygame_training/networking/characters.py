import pygame, random, logging
from pygame.locals import *
from name_tag import Name_tag

# CONSTANTS
#MAGE = 1
MAGE = "Mage"

class Avatar(pygame.sprite.Sprite):
    def __init__(self, screen, level, name, type):
        super().__init__()
        self.name = name
        self.character_type = type
        self.level = level
        self.image = self._load_image()
        self.screen = screen
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
        self.movement_speed = 7  # number of pixels traveled per frame
        self.looking_right = 0
        # Dictionary containing key bindings to functions and their arguments
        self.keys_map = {
            K_w: (self.move_avatar, (0, -self.movement_speed)),
            K_s: (self.move_avatar, (0, self.movement_speed)),
            K_a: (self.move_avatar, (-self.movement_speed, 0)),
            K_d: (self.move_avatar, (self.movement_speed, 0))
        }
        self.name_tag = Name_tag(name, self.screen, font_size=int(self.rect.height / 3))
        self.collided = 0  # List of sprites which are in contact with player
        self.curent_tile = 0  # Tile occupied by player at the moment
        self.world_coords = (100, 100)
        self.spawn()
        logging.info("avatar {} spawned".format(self.name))

    def get_meta_data(self):
        return {
            "name": self.name,
            "world_coords": self.world_coords,
            "type": self.character_type
        }

    def _load_image(self, path="../game_sprites/"):
        if self.character_type == MAGE:
            path += "mage.png"
        try:
            return pygame.image.load(path).convert_alpha()
        except:
            image = pygame.Surface((50, 100))
            image.fill((255, 255, 25))
            return image

    def move_avatar(self, delta):
        """Moves the sprite on screen and updates sprite to face the right direction
        Delta is a tuple
        The method first assigns player's global position and then calculates where he should appear on the window"""
        new_world_x = self.world_coords[0] - delta[0]
        new_world_y = self.world_coords[1] - delta[1]
        if (-self.level.LEVEL_WIDTH_PX <= new_world_x <= 0 and -self.level.LEVEL_HEIGHT_PX <= new_world_y <= 0
            and self._check_pos(new_world_x, new_world_y)):
            self.world_coords = [new_world_x, new_world_y]
        # Turn image right or left
        if delta[0] < 0 and self.looking_right:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.looking_right = not self.looking_right
        elif delta[0] > 0 and not self.looking_right:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.looking_right = not self.looking_right

    def press_key(self, key):
        """Key must be keyboard key defined in pygame.locals constants
        Gets function from keys_map and calls it with arguments stored in same dictionary"""
        if key in self.keys_map:
            self.keys_map[key][0](self.keys_map[key][1])

    def update(self):
        #self.rect.centerx, self.rect.centery = self.level.x_offset - self.world_coords[0], self.level.y_offset - self.world_coords[1]
        self.rect.centerx, self.rect.centery = self.level.x_offset - self.world_coords[0], self.level.y_offset - self.world_coords[1]
        self._check_map_borders()
        # Calculate text's Y coordinate so it's right above sprite's head
        self.name_tag.update_pos((self.rect.left, self.rect.center[1] - self.rect.height / 2))
        self.name_tag.render()
        #self._check_pos()

    def _check_pos(self, x, y):
        """This method returns false if player is colliding with unwalkable tiles"""
        x, y = int((-x) / self.level.TILE_SIZE), int(-y / self.level.TILE_SIZE)
        #logging.info("{}: x {}, y {}, width {} height {}".format(str(self.level.LEVEL[x * self.level.LEVEL_HEIGHT + y].walkable),
        #                                                         x, y, self.level.LEVEL_WIDTH, self.level.LEVEL_HEIGHT))
        return self.level.LEVEL[x * self.level.LEVEL_HEIGHT + y].walkable

    def _check_map_borders(self):
        """This method is responsible for all actions related to player position"""
        # self.rect.clamp_ip(self.screen.get_rect())  # Doesn't allow player to move beyond the screen
        if self.rect.centerx >= self.screen.get_width() - self.level.margin:
            self.level.move_map((-self.movement_speed, 0))
        if self.rect.centerx <= self.level.margin:
            self.level.move_map((self.movement_speed, 0))
        if self.rect.centery >= self.screen.get_height() - self.level.margin:
            self.level.move_map((0, -self.movement_speed))
        if self.rect.centery <= self.level.margin:
            self.level.move_map((0, self.movement_speed))

    def spawn(self):
        """Spwans avatar in a random location on the map
        Warning, coordinates ust be divisible by player step, otherwise it will cause
        an array out of bounds exception near edge of the map"""
        # TODO fix a bug where player can be spawned in unwalkable tile.
        self.world_coords= [-self.movement_speed, -self.movement_speed]


class GuestAvatar(Avatar):
    """Must be initialized on HOST machine"""
    def __init__(self, surface, level, name, character_type):
        super(GuestAvatar, self).__init__(surface, level, name, character_type)

    def _check_map_borders(self):
        """Must be empty!"""
        pass


class GuestMage(GuestAvatar):
    def __init__(self, surface, level, name, character_type):
        super(GuestMage, self).__init__(surface, level, name, character_type)


class Mage(Avatar):
    def __init__(self, surface, level, name, character_type):
        super(Mage, self).__init__(surface, level, name, character_type)

    def _load_image(self, path="../game_sprites/mage.png"):
        try:
            return pygame.image.load(path).convert_alpha()
        except pygame.error:
            image = pygame.Surface((50, 100))
            image.fill((255, 255, 25))
            return image


class ClientAvatar(Avatar):
    def __init__(self, screen, level, name, character_type):
        super(ClientAvatar, self).__init__(screen, level, name, character_type)

    def press_key(self, key):
        pass

    #def update(self):
     #   #self.world_coords = (self.level.x_offset - self.rect.centerx, self.level.y_offset - self.rect.centery)
      #  # Calculate text's Y coordinate so it's right above sprite's head
       # self.name_tag.update_pos((self.rect.left, self.rect.center[1] - self.rect.height / 2))
        #self.name_tag.render()
        #"""Should translate world coords into rectX and rectY"""
        #self.rect.centerx, self.rect.centery = -self.world_coords[0] + self.level.x_offset, \
          #                         -self.world_coords[1] + self.level.y_offset


TYPES_MAP = {
    MAGE: Mage
}