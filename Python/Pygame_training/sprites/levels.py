import random
import pygame
from pygame.locals import *


class Level:
    """Class responsible for generating, storing, and updating background level"""
    def __init__(self, surface, players, tile_size=50, level_width=50, level_height=50):
        self.LEVEL = []
        self.surface = surface
        self.players = players
        self.TILE_SIZE = tile_size  # tile size in pixels
        self.LEVEL_WIDTH = level_width  # number of tiles horizontally
        self.LEVEL_HEIGHT = level_height  # number of tiles vertically
        self.KEYS_MAP = {}
        self.x_offset, self.y_offset = 0, 0  # Used to move map around
        self.x_offset_step, self.y_offset_step = 45, 45
        # when player approaches any end by margin pixels, map will respond and move accordingly
        self.margin = 100
        self._generate_level()

    def _generate_level(self):
        """Generates ranndom colored tiles"""
        for t in range(self.LEVEL_WIDTH * self.LEVEL_HEIGHT):
            rand_color = (random.randint(0, 0xff), random.randint(0, 0xff), random.randint(0, 0xff))
            self.LEVEL.append(rand_color)
        self.LEVEL[0] = (0xff, 0xff, 0xff)
        self.LEVEL[self.LEVEL_WIDTH * self.LEVEL_HEIGHT - 1] = (0, 0, 0)

    def draw_level(self):
        # TODO update only area curently viwed by player
        # TODO update only part of the screen that changed since lsat frame e.g. player moved
        # to get [x][y] use formula (x * width + y)
        for tile in range(len(self.LEVEL)):  # Tile is an index in list of tiles
            x = int(tile / self.LEVEL_HEIGHT) * self.TILE_SIZE
            y = (tile % self.LEVEL_HEIGHT) * self.TILE_SIZE
            pygame.draw.rect(self.surface, self.LEVEL[tile],
                             (x + self.x_offset, y + self.y_offset, self.TILE_SIZE, self.TILE_SIZE))

    def press_key(self, key):
        if key in self.KEYS_MAP:
            self.KEYS_MAP[key]()

    def move_map(self, direction):
        self.x_offset += direction[0]
        self.y_offset += direction[1]

    def update(self):
        self._check_pos()

    def _check_pos(self):
        for player in self.players:
            if player.rect.x >= self.surface.get_width() - self.margin:
                self.move_map((-player.movement_speed, 0))
            if player.rect.x <= self.margin:
                self.move_map((player.movement_speed, 0))
            if player.rect.y >= self.surface.get_height() - self.margin:
                self.move_map((0, -player.movement_speed))
            if player.rect.y <= self.margin:
                self.move_map((0, player.movement_speed))
