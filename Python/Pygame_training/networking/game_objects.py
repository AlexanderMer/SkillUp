import pygame


class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = self.load_image()
        self.rect = self.image.get_rect()

    def load_image(self, path="../game_sprites/crosshair.png"):
        try:
            return pygame.image.load(path).convert_alpha()
        except:
            image = pygame.Surface((25, 25))
            image.fill((255, 255, 255))
            return image