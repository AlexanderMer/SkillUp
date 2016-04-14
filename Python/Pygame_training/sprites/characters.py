import pygame, random
from pygame.locals import *
from name_tag import Name_tag


class Block(pygame.sprite.Sprite):

    def __init__(self, screen, min_size, max_size, colour=0):
        super().__init__()
        size = random.randint(min_size, max_size)
        self.image = pygame.Surface((size, size))
        self.image.fill(colour if colour != 0 else self._random_color())
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = random.randint(0, 700), random.randint(0, 500)
        self.speedx, self.speedy = random.randint(-17, 17), random.randint(-17, 17)

    def update(self):
        """This function must be called each frame for movement and collision testing"""
        self.rect.left += self.speedx
        self.rect.top += self.speedy
        if self.rect.right > self.screen.get_width() or self.rect.left < 0:
            self.speedx = -self.speedx
        if self.rect.bottom > self.screen.get_height() or self.rect.top < 0:
            self.speedy = -self.speedy

    def _random_color(self):
        """returns a tuple prepresenting a random color in the following format (r, g, b)"""
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Mage(pygame.sprite.Sprite):

    def __init__(self, screen, name):
        super().__init__()
        self.image = self._load_image()
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = int(screen.get_size()[0] / 2), int(screen.get_size()[1] / 2)
        self.velocity = [0, 0]
        self.movement_speed = 7  # number of pixels traveled per frame
        self.looking_right = 0
        # Dictionary containing key bindings to functions and their arguments
        self.keys_map = {
            K_w: (self.move, (0, -self.movement_speed)),
            K_s: (self.move, (0, self.movement_speed)),
            K_a: (self.move, (-self.movement_speed, 0)),
            K_d: (self.move, (self.movement_speed, 0))
        }
        self.name_tag = Name_tag(name, font_size=int(self.rect.height / 3))


    def _load_image(self, path="sprites/mage.png"):
        try:
            return pygame.image.load(path)
        except:
            image = pygame.Surface((50, 100))
            image.fill((255, 255, 25))
            return image

    def move(self, delta):
        """Moves the sprite on screen and updates sprite to face the right direction"""
        "Delta is a tuple"
        if delta[0] < 0 and self.looking_right:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.looking_right = not self.looking_right
        elif delta[0] > 0 and not self.looking_right:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.looking_right = not self.looking_right
        self.rect.x += delta[0]
        self.rect.y += delta[1]

    def press_key(self, key):
        """Gets function from keys_map and calls it with arguments stored in same dictionary"""
        if key in self.keys_map:
            self.keys_map[key][0](self.keys_map[key][1])

    def update(self):
        self.rect.clamp_ip(self.screen.get_rect())  # Doesn't allow player to move beyond the screen
        # Calculate Y coordinate so it's right above sprite's head
        self.name_tag.update_pos((self.rect.left, self.rect.center[1] - self.rect.height / 2))
        self.screen.blit(self.name_tag.marked_text_surface, self.name_tag.marked_text_rect)
        self.screen.blit(self.name_tag.text_surface, self.name_tag.text_rect)
