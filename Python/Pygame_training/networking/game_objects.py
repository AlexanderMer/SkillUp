import pygame, logging, colours, time


class GameObject(pygame.sprite.Sprite):
    def __init__(self, world_coords):
        super().__init__()
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.world_coords = world_coords

    def load_image(self, path=0):
        #if not path:
        #    path = self.image_path
        #try:
        #    return pygame.image.load(path).convert_alpha()
        #except:
        image = pygame.Surface((25, 25))
        image.fill(colours.random_color())
        return image


class HealthBar():
    """Health bar representing HP in %"""
    def __init__(self, player, surface):
        self.surface = surface
        self.player = player
        self.width = player.rect.width
        self.height = player.rect.height


    def update(self):
        bg_pos = (self.player.rect.left, self.player.rect.top, self.player.rect.width, 10)
        fg_pos = (self.player.rect.left, self.player.rect.top,
                  self.player.rect.width - (self.player.rect.width /  (100 / (101 - self.player.health))), 10)
        pygame.draw.rect(self.surface, colours.RED, bg_pos)
        pygame.draw.rect(self.surface, colours.GREEN, fg_pos)


class Crosshair(GameObject):
    def __init__(self):
        self.image_path = "../game_sprites/crosshair.png"
        super(Crosshair, self).__init__(pygame.mouse.get_pos())


    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Projectile(GameObject):
    def __init__(self, level, world_coords, lifetime=5):
        super(Projectile, self).__init__(world_coords)
        self.level = level
        self.speed = 12  # Number of pixels projectile moves per update
        self.velocity = [0, 0]
        self.bday = time.time()
        self.lifetime = lifetime
        #logging.info("Projectile created")

    def update(self):
        if time.time() - self.bday > self.lifetime:
            self.kill()
        self.world_coords = [w + v for w, v in zip(self.world_coords, self.velocity)]
        self.rect.center = (self.level.x_offset - self.world_coords[0], self.level.y_offset - self.world_coords[1],)
        if (not 0 <= -self.world_coords[0] <= self.level.LEVEL_WIDTH_PX or
                not 0 <= -self.world_coords[1] <= self.level.LEVEL_HEIGHT_PX):
            self.kill()
            #logging.info("projectile {} killed".format(self))

    def on_collide(self, player):
        pass


class CharProjectile(Projectile):
    def __init__(self, char, level, lifetime=5, font='freesansbold.ttf', font_size = 30):
        super(CharProjectile, self).__init__(level, lifetime)
        self.char = char
        self.text_string = char
        self.fontObj = pygame.font.Font(font, font_size)
        self.text_surface = self.fontObj.render(self.text_string, True, colours.GREEN, colours.BLUE)
        self.text_rect = self.text_surface.get_rect()

    def update(self, surface):
    # Updates position based on velocity
        Projectile.update(self)

projectiles = pygame.sprite.Group()
