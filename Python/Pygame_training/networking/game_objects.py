import pygame, logging, colours


class GameObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.world_coords = [0, 0]

    def load_image(self, path=0):
        if not path:
            path = self.image_path
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
    def __init__(self):
        super(Projectile, self).__init__()
        self.velocity = [0, 0]
        logging.info("Projectile created")

    def update(self, players):
        self.world_coords = [w + v for w, v in zip(self.world_coords, self.velocity)]
        collided = pygame.sprite.spritecollide(self.rect, players)
        if collided:
            for player in collided:
                self.on_collide(player)

    def on_collide(self, player):
        pass

