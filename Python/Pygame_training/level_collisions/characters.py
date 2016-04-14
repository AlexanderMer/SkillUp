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

    def __init__(self, screen, level, name):
        super().__init__()
        self.level = level
        self.image = self._load_image()
        self.screen = screen
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
        self.movement_speed = 7  # number of pixels traveled per frame
        self.looking_right = 0
        # Dictionary containing key bindings to functions and their arguments
        self.keys_map = {
            K_w: (self.move_character, (0, -self.movement_speed)),
            K_s: (self.move_character, (0, self.movement_speed)),
            K_a: (self.move_character, (-self.movement_speed, 0)),
            K_d: (self.move_character, (self.movement_speed, 0))
        }
        self.name_tag = Name_tag(name, font_size=int(self.rect.height / 3))
        self.spawn()

    def _load_image(self, path="sprites/mage.png"):
        try:
            return pygame.image.load(path).convert_alpha()
        except:
            image = pygame.Surface((50, 100))
            image.fill((255, 255, 25))
            return image

    def move_character(self, delta):
        """Moves the sprite on screen and updates sprite to face the right direction
        Delta is a tuple"""
        # move
        self.rect.x += delta[0]
        self.rect.y += delta[1]
        # Turn image right or left
        if delta[0] < 0 and self.looking_right:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.looking_right = not self.looking_right
        elif delta[0] > 0 and not self.looking_right:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.looking_right = not self.looking_right

    def press_key(self, key):
        """Gets function from keys_map and calls it with arguments stored in same dictionary"""
        if key in self.keys_map:
            self.keys_map[key][0](self.keys_map[key][1])

    def update(self):
        self.collided = pygame.sprite.spritecollide(self, self.level.sprite_group, 65)
        self._check_pos()
        self.rect.clamp_ip(self.screen.get_rect())  # Doesn't allow player to move beyond the screen
        # Calculate Y coordinate so it's right above sprite's head
        self.name_tag.update_pos((self.rect.left, self.rect.center[1] - self.rect.height / 2))
        self.screen.blit(self.name_tag.marked_text_surface, self.name_tag.marked_text_rect)
        self.screen.blit(self.name_tag.text_surface, self.name_tag.text_rect)



    def _check_pos(self):
        """This method is responceble for all actions related to player position"""
        if self.rect.x >= self.screen.get_width() - self.level.margin:
            self.level.move_map((-self.movement_speed, 0))
        if self.rect.x <= self.level.margin:
            self.level.move_map((self.movement_speed, 0))
        if self.rect.y >= self.screen.get_height() - self.level.margin:
            self.level.move_map((0, -self.movement_speed))
        if self.rect.y <= self.level.margin:
                self.level.move_map((0, self.movement_speed))


    def spawn(self):
        self.rect.center = (random.randint(0, self.level.LEVEL_WIDTH_PX), random.randint(0, self.level.LEVEL_HEIGHT_PX))

