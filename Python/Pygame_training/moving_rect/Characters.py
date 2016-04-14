import pygame
from pygame.locals import *

class Player(pygame.Rect):
    def __init__(self, display_surf):
        super().__init__(32, 32, 125, 79)
        self.step_size = 15
        self.keys_map = {
            K_w: (0, -self.step_size),
            K_s: (0, self.step_size),
            K_a: (-self.step_size, 0),
            K_d: (self.step_size, 0)
        }
        self.relative_xy_offset = (self.x, self.y)
        image_name = 'cat.png'
        self.display_surf = display_surf
        try:
            self.image = pygame.image.load(image_name)
        except IOError:
            print('failed to load image {}'.format(image_name))
        else:
            print('Image loaded')

    def press_key(self, key):
        if key in self.keys_map:
            self.move(self.keys_map[key])

    def move(self, delta):
        # takes a tuple as delata (x, y)
        self.x += delta[0]
        self.y += delta[1]
        self.display_surf.blit(self.image, (self.x, self.y))


