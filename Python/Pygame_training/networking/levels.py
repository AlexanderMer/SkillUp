import pygame, random, pickle, colours


class Tile(pygame.sprite.Sprite):
    def __init__(self, image_path, walkable=True, tile_id=1):
        super().__init__()
        try:
            self.image = pygame.image.load(image_path).convert()
        except pygame.error:
            self.image = pygame.Surface((50, 50))
            self.image.fill(colours.random_color())
        self.rect = self.image.get_rect()
        self.tile_id = tile_id
        self.walkable =walkable


#TODO make level savable and loadable in JSON formats (pickle causes weird bugs, suspect becauseduring loading
#instances get messed up# )
class Sprite_Level:
    """Class responsible for generating, storing, and updating background level"""
    def __init__(self, surface, tile_size=250, level_width=5, level_height=5):
        self.LEVEL = []
        self.surface = surface
        self.LEVEL_WIDTH = level_width  # number of tiles horizontally
        self.LEVEL_HEIGHT = level_height  # number of tiles vertically
        self.sprite_group = pygame.sprite.Group()
        self.generate_level_test()
        #self.load_level()
        self.TILE_SIZE = self.LEVEL[0].rect.width  # tile size in pixels
        self.LEVEL_WIDTH_PX = self.TILE_SIZE * self.LEVEL_WIDTH  # Width in pixels
        self.LEVEL_HEIGHT_PX = self.TILE_SIZE * self.LEVEL_HEIGHT  # Height in pixels
        self.KEYS_MAP = {}
        self.x_offset, self.y_offset = 0, 0  # Used to move map around
        self.x_offset_step, self.y_offset_step = 45, 45  # Speed with which map actually moves
        self.margin = 100  # when player approaches any end by margin pixels, map will respond and move accordingly
        # self.load_level()

    def save_json(self):
        pass

    def load_json(self):
        pass

    def generate_level_test(self):
        random.seed(32)
        for t in range(self.LEVEL_WIDTH * self.LEVEL_HEIGHT):
            tile = Tile("../game_sprites/grass.png", tile_id=t) if random.random() < 0.92 else \
                Tile("../game_sprites/water.png", walkable=False, tile_id=t)
            self.LEVEL.append(tile)
            self.sprite_group.add(tile)
        #with open("level.lvl", "wb") as f:
        #    pickle.dump(self.LEVEL, f)
        #with open("level_sprites.lvl", "wb") as f:
        #    pickle.dump(self.sprite_group, f)
        #print("File dumbped!!")

    def load_level(self, path="level.lvl"):
        with open("level.lvl", "rb") as f:
            self.LEVEL = pickle.load(f)
        for tile in self.LEVEL:
            self.sprite_group.add(tile)

    def _generate_level(self):
        """Generates ranndom colored tiles"""
        for t in range(self.LEVEL_WIDTH * self.LEVEL_HEIGHT):
            tile = Tile("sprites/grass.png")
            self.LEVEL.append(tile)
            self.sprite_group.add(tile)
        self.LEVEL[0].image.fill((0xff, 0xff, 0xff))
        self.LEVEL[self.LEVEL_WIDTH * self.LEVEL_HEIGHT - 1].image.fill((0, 0, 0))

    def draw_level(self):
        #self.sprite_group.draw(self.surface)
        # TODO update only area curently viwed by player
        # TODO update only part of the screen that changed since lsat frame e.g. player moved
        # to get [x][y] use formula (x * height + y)
        for tile in range(len(self.LEVEL)):  # Tile is an index in list of tiles
            x = int(tile / self.LEVEL_HEIGHT) * self.TILE_SIZE
            y = (tile % self.LEVEL_HEIGHT) * self.TILE_SIZE
            self.LEVEL[tile].rect.x = x + self.x_offset
            self.LEVEL[tile].rect.y = y + self.y_offset
        self.sprite_group.draw(self.surface)

    def press_key(self, key):
        if key in self.KEYS_MAP:
            self.KEYS_MAP[key]()

    def move_map(self, direction):
        # if statements make sure maps doesn't move outside it's boundaries
        self.x_offset += direction[0]
        self.y_offset += direction[1]
        if (self.x_offset > 0 or self.y_offset > 0
                or self.x_offset < -(self.LEVEL_WIDTH_PX - self.surface.get_width())
                or self.y_offset < -(self.LEVEL_HEIGHT_PX - self.surface.get_height())):
            self.x_offset -= direction[0]
            self.y_offset -= direction[1]
        # print("{} {}".format(self.x_offset, self.y_offset))

    def update(self):
        self.draw_level()

