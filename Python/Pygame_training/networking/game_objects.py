import pygame, logging, colours, time


class GameObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.world_coords = [100, 100]


    def load_image(self, path="..\game_sprites\game_object.png"):
        try:
            return pygame.image.load(path).convert_alpha()
        except:
            image = pygame.Surface((25, 25))
            image.fill(colours.random_color())
            return image


class Crosshair(GameObject):
    def __init__(self):
        self.image_path = "../game_sprites/crosshair.png"
        super(Crosshair, self).__init__()


    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Projectile(GameObject):
    def __init__(self, level):
        super(Projectile, self).__init__()
        self.level = level
        self.speed = 12  # Number of pixels projectile moves per update
        self.velocity = [0, 0]
        self.bday = time.time()
        logging.info("Projectile created")

    def update(self):
        if time.time() - self.bday > 5:
            self.kill()
        self.world_coords = [w + v for w, v in zip(self.world_coords, self.velocity)]
        self.rect.center = (self.level.x_offset - self.world_coords[0], self.level.y_offset - self.world_coords[1],)
        if not 0 <= -self.world_coords[0] <= self.level.LEVEL_WIDTH_PX or not 0 <= -self.world_coords[1] <= self.level.LEVEL_HEIGHT_PX:
            self.kill()
            logging.info("projectile {} killed".format(self))

    def on_collide(self, player):
        pass

    def kill_projectile(self):
        self.kill()


class CharProjectile(Projectile):
    def __init__(self, char, level):
        super(CharProjectile, self).__init__(level)
        self.char = char

