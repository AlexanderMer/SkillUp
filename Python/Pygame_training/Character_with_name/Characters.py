import pygame
from pygame.locals import *
from name_tag import name_tag

class Player(pygame.Rect):
    def __init__(self, display_surf, name):
        super().__init__(100, 100, 125, 79)
        self.step_size = 15
        self.keys_map = {
            K_w: (0, -self.step_size),
            K_s: (0, self.step_size),
            K_a: (-self.step_size, 0),
            K_d: (self.step_size, 0)
        }
        self.relative_xy_offset = (self.x, self.y)
        self.display_surf = display_surf
        self.load_image()
        self.name = name_tag(name)

    def press_key(self, key):
        if key in self.keys_map:
            self.move(self.keys_map[key])

    def tick(self):
        pygame.draw.rect(self.display_surf, (0xff, 0, 0), self)
        self.center = pygame.mouse.get_pos()

    def load_image(self):
        image_name = 'player.png'
        try:
            self.image = pygame.image.load(image_name)
        except IOError:
            print('failed to load image {}'.format(image_name))
        else:
            print('Image loaded')

    def move(self, delta):
        # takes a tuple as delata (x, y)
        self.x += delta[0]
        self.y += delta[1]
        self.display_surf.blit(self.image, (self.x, self.y))