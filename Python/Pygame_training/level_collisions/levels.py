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


class Sprite_Level:
    """Class responsible for generating, storing, and updating background level"""
    def __init__(self, surface, tile_size=100, level_width=50, level_height=50):
        self.LEVEL = []
        self.surface = surface
        self.TILE_SIZE = tile_size  # tile size in pixels
        self.LEVEL_WIDTH = level_width  # number of tiles horizontally
        self.LEVEL_HEIGHT = level_height  # number of tiles vertically
        self.LEVEL_WIDTH_PX = self.TILE_SIZE * self.LEVEL_WIDTH  # Width in pixels
        self.LEVEL_HEIGHT_PX = self.TILE_SIZE * self.LEVEL_HEIGHT  # Height in pixels
        self.sprite_group = pygame.sprite.Group()
        self.KEYS_MAP = {}
        self.x_offset, self.y_offset = 0, 0  # Used to move map around
        self.x_offset_step, self.y_offset_step = 45, 45
        self.margin = 100  # when player approaches any end by margin pixels, map will respond and move accordingly
        # self.load_level()
        self.generate_level_test()


    def generate_level_test(self):
        for t in range(self.LEVEL_WIDTH * self.LEVEL_HEIGHT):
            tile = Tile("sprites/grass.png", tile_id=t) if random.random() < 0.92 else Tile("sprites/water.png", walkable=False, tile_id=t)
            self.LEVEL.append(tile)
            self.sprite_group.add(tile)


    def load_level(self, path="level.lvl"):
        try:
            with open(path, "rb") as lvl:
                self.LEVEL = pickle.load(lvl)
        except IOError:
            self._generate_level()

    def _generate_level(self):
        """Generates ranndom colored tiles"""
        for t in range(self.LEVEL_WIDTH * self.LEVEL_HEIGHT):
            tile = Tile("sprites/grass.png")
            self.LEVEL.append(tile)
            self.sprite_group.add(tile)
        self.LEVEL[0].image.fill((0xff, 0xff, 0xff))
        self.LEVEL[self.LEVEL_WIDTH * self.LEVEL_HEIGHT - 1].image.fill((0, 0, 0))
        print(*self.sprite_group)

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

